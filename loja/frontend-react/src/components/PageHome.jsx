import React from "react";

export function PageHome() {
  return (
    <div className="flex flex-col items-center justify-center pt-32 text-center select-none">

      {/* Título principal */}
      <h1 className="text-white text-6xl font-bold tracking-wider drop-shadow-[0_4px_8px_rgba(0,0,0,0.8)]">
        GUY'S CONCESSIONÁRIA
      </h1>

      {/* Subtítulo elegante */}
      <p className=" absolute
        text-white 
        text-3xl
        left-10 
        top-30
        font-light 
        tracking-wide 
        drop-shadow-[0_2px_6px_rgba(0,0,0,0.8)]
        font-poppins
      ">
        Carros de luxo você encontra aqui!
      </p>

    </div>
  );
}
