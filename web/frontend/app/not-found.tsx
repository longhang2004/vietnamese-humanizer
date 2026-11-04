import Link from "next/link";
export default function NotFound() {
  return <section className="page-heading py-24"><h1>Chưa tìm thấy trang này.</h1><p>Đường dẫn có thể đã thay đổi. Bạn có thể về trang chủ hoặc tiếp tục soát văn bản.</p><div className="mt-8 flex flex-wrap gap-3"><Link className="button-primary" href="/">Về trang chủ</Link><Link className="button-secondary" href="/check">Soát văn bản</Link></div></section>;
}
