import React, { useState } from "react";
import axios from "axios";

const ImageUpload = ({ setSimilarImages }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [model, setModel] = useState("resnet");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleModelChange = (event) => {
    setModel(event.target.value);
  };

  const handleSearch = async () => {
    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("model_name", model);

    const response = await axios.post("http://localhost:8000/search/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    setSimilarImages(response.data.similar_images);
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <select value={model} onChange={handleModelChange}>
        <option value="resnet">ResNet</option>
        <option value="vgg">VGG</option>
        {/* Add more models here */}
      </select>
      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default ImageUpload;
