import type { ReactNode } from "react";
import styles from "./ReadingLayout.module.css";

type ContentsItem = { href: string; label: string };

export function ReadingHeader({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <header className={`page-heading ${styles.header}`}>
      <h1>{title}</h1>
      <p>{children}</p>
    </header>
  );
}

export function ReadingLayout({
  title,
  introduction,
  contents,
  contentsLabel,
  children,
}: {
  title: string;
  introduction: ReactNode;
  contents: ContentsItem[];
  contentsLabel: string;
  children: ReactNode;
}) {
  return (
    <div className={styles.readingPage}>
      <ReadingHeader title={title}>{introduction}</ReadingHeader>
      <div className={styles.layout}>
        <nav className={styles.index} aria-label={contentsLabel}>
          <ul>
            {contents.map((item) => (
              <li key={item.href}>
                <a href={item.href}>{item.label}</a>
              </li>
            ))}
          </ul>
        </nav>
        <article className={`prose-content ${styles.article}`}>
          {children}
        </article>
      </div>
    </div>
  );
}
