
import React from "react";

const SimilarImages = ({ images }) => {
  return (
    <div className="image-results">
      {images.map((image, index) => (
        <img key={index} src={image} alt={`Similar ${index}`} />
      ))}
    </div>
  );
};

export default SimilarImages;