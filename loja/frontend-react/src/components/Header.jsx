export default function Header({ title, subtitle }) {
  return (
    <header className="text-white select-none">
      <h1 className="text-4xl font-semibold">{title}</h1>

      <div className="overflow-hidden inline-block">
        <h1
          className="
            text-6xl font-light tracking-wide
            transition-all duration-300 ease-out
            hover:scale-105 hover:tracking-widest
            cursor-default
          "
          style={{ fontFamily: "'Oswald', sans-serif" }}
        >
          {subtitle}
        </h1>
      </div>
    </header>
  );
}
