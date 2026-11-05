import Link from "next/link";
import styles from "../components/ReadingLayout.module.css";

export default function NotFound() {
  return (
    <section className={styles.recovery}>
      <h1>Chưa tìm thấy trang này.</h1>
      <p>
        Đường dẫn có thể đã thay đổi. Bạn có thể về trang chủ hoặc tiếp tục soát
        văn bản.
      </p>
      <div className={styles.actions}>
        <Link className="button-primary" href="/">
          Về trang chủ
        </Link>
        <Link className="button-secondary" href="/check">
          Soát văn bản
        </Link>
      </div>
    </section>
  );
}
