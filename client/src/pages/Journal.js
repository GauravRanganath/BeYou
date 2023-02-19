import Webcam from "../components/Webcam.js";
import './../index.css'

const Journal = () => {
  return (
    <>
      <p className="question">How was your day?</p>
      <Webcam />
    </>
  );
};

export default Journal;
