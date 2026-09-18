from __future__ import annotations

import ipaddress

from starlette.types import ASGIApp, Receive, Scope, Send

from app.config import settings

_PRIVATE_PROXY_NETWORKS = (
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "127.0.0.0/8",
    "fe80::/10",
    "::1",
)


def _parse_raw_hosts(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse_host_port(value: str) -> tuple[str, int]:
    if value.startswith("["):
        bracket_end = value.find("]")
        if bracket_end == -1:
            return value, 0
        host = value[1:bracket_end]
        remainder = value[bracket_end + 1 :]
        if not remainder:
            return host, 0
        if not remainder.startswith(":"):
            return value, 0
        try:
            return host, int(remainder[1:])
        except ValueError:
            return host, 0

    if value.count(":") == 1:
        host, port = value.rsplit(":", 1)
        try:
            return host, int(port)
        except ValueError:
            return value, 0

    return value, 0


class TrustedProxyHosts:
    """Allowlist of proxy hops: literals, addresses, and CIDR networks."""

    def __init__(self, trusted_hosts: list[str] | str) -> None:
        self.always_trust = trusted_hosts in ("*", ["*"])
        self.trusted_literals: set[str] = set()
        self.trusted_addresses: set[ipaddress.IPv4Address | ipaddress.IPv6Address] = set()
        self.trusted_networks: set[ipaddress.IPv4Network | ipaddress.IPv6Network] = set()
        if self.always_trust:
            return
        hosts = _parse_raw_hosts(trusted_hosts) if isinstance(trusted_hosts, str) else trusted_hosts
        for host in hosts:
            if "/" in host:
                try:
                    self.trusted_networks.add(ipaddress.ip_network(host, strict=False))
                except ValueError:
                    self.trusted_literals.add(host.casefold())
                continue
            try:
                self.trusted_addresses.add(ipaddress.ip_address(host))
            except ValueError:
                self.trusted_literals.add(host.casefold())

    def __contains__(self, host: str | None) -> bool:
        if self.always_trust:
            return True
        if not host:
            return False
        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            return host.casefold() in self.trusted_literals
        return ip in self.trusted_addresses or any(
            ip in network for network in self.trusted_networks
        )

    def get_trusted_client_address(self, x_forwarded_for: str) -> tuple[str, int]:
        hosts = _parse_raw_hosts(x_forwarded_for)
        if not hosts:
            return "", 0
        if self.always_trust:
            return _parse_host_port(hosts[0])
        for host_port in reversed(hosts):
            host, port = _parse_host_port(host_port)
            if host not in self:
                return host, port
        return _parse_host_port(hosts[0])


def _configured_trusted_hosts() -> TrustedProxyHosts:
    configured = settings.TRUSTED_PROXY_HOSTS.strip()
    if configured == "*":
        return TrustedProxyHosts("*")
    hosts = _parse_raw_hosts(configured)
    if settings.TRUST_PRIVATE_PROXIES:
        hosts.extend(_PRIVATE_PROXY_NETWORKS)
    return TrustedProxyHosts(hosts or ["127.0.0.1"])


def proxy_peer_is_trusted(peer: str) -> bool:
    return peer in _configured_trusted_hosts()


def forwarded_client_host(peer: str, forwarded: str) -> str:
    hosts = _configured_trusted_hosts()
    if peer not in hosts:
        return peer
    host, _port = hosts.get_trusted_client_address(forwarded)
    return host or peer


class TrustedProxyHeadersMiddleware:
    """Rewrite client address from X-Forwarded-For only for allowlisted peers.

    Walks the header right-to-left and skips trusted hops so the rate limiter
    keys on the connecting client, not an intermediate proxy.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            client = scope.get("client")
            peer = client[0] if client else ""
            hosts = _configured_trusted_hosts()
            if peer in hosts:
                headers = {
                    key.decode("latin-1"): value.decode("latin-1")
                    for key, value in scope.get("headers", [])
                }
                forwarded = headers.get("x-forwarded-for")
                if forwarded:
                    host, port = hosts.get_trusted_client_address(forwarded)
                    if host:
                        scope["client"] = (host, port or (client[1] if client else 0))
        await self.app(scope, receive, send)
