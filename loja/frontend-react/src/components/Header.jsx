export default function Header({ title, subtitle }) {
  return (
    <header className="text-white select-none">
      <h1 className="text-4xl font-semibold">{title}</h1>

      <div className="inline-block">
        <h1
          className="
            absolute 
            font-light tracking-wide
            transition-all top-50 duration-300 ease-out
            hover:scale-105 hover:tracking-wide
            
          "
        >
          {subtitle}
        </h1>
      </div>
    </header>
  );
}
