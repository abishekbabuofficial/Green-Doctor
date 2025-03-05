import React, { useState } from "react";
import "./about.css";
import ImageCard from '../ImageCard';
import header from "../../img/header.png";

function About() {
  const CardData = [
    {
      id : 1,
      imageSrc : '',
      name: "GURUNATHAN T",
      role: "Fronted Developer",
      linkedin : "https://www.linkedin.com/in/gurunathan-t/",
      insta:"#",
      github:"https://github.com/Gurunathan2412",
    },
    {
      id : 2,
      imageSrc : '',
      name: "SRINIVASAN S R",
      role: "Designer",
      linkedin : "https://www.linkedin.com/in/srinivasan-s-r-534544226/",
      insta:"#",
      github:"https://github.com/srinivas232003",
      
    },
    {
      id : 3,
      imageSrc : '',
      name: "ABISHEK B",
      role: "Fronted Developer",
      linkedin : "https://www.linkedin.com/in/abishek-babu-career/",
      insta:"#",
      github:"https://github.com/abishekbabuofficial",
    },
    
  ];
  return (
    <>
    <h1 id="img-h1">Our Team</h1>
    <img id="one" src={header} alt="" />
    <div className="images">
      {CardData.map((card) => (
        <ImageCard
          key={card.id}
          // imageSrc={card.imageSrc}
          name={card.name}
          role={card.role}
          linkedin={card.linkedin}
          insta={card.insta}
          github={card.github}
        />
      ))}
    </div>
    </>
  );
}
export default About;
