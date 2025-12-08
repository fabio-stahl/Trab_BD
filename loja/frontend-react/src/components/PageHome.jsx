import React from "react";

export function PageHome() {
  return (
    <div className="flex flex-col items-center justify-center pt-20 text-center select-none">

      {/* Título principal */}
      <h1 className=" absolute text-white text-6xl left-10 top-50 font-bold tracking-wide">
        GUY'S CONCESSIONÁRIA
      </h1>

      {/* Subtítulo elegante */}
      <p className="absolute top-70 left-12 text-white text-2xl mt-4 font-light tracking-wide font-poppins">
        Carros de luxo você encontra aqui!
      </p>
    </div>
  );
}
