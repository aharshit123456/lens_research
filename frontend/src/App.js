import React, { useState } from "react";
import ImageUpload from "./components/ImageUpload";
import SimilarImages from "./components/SimilarImages";

function App() {
  const [similarImages, setSimilarImages] = useState([]);

  return (
    <div>
      <h1>Image Similarity Search</h1>
      <ImageUpload setSimilarImages={setSimilarImages} />
      <SimilarImages images={similarImages} />
    </div>
  );
}

export default App;
