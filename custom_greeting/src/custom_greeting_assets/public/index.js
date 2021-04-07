import { render } from "react-dom";
import axios from "axios";
import * as React from "react";

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedFile: null,
      goodData: "good",
      badData: "bad",
    };

    this.onCheckFile = this.onCheckFile.bind(this);
  }

  onResult = () => {
    window.open("http://localhost:5000/checkPDF");
  };
  // On file select (from the pop up)
  onFileChange = (event) => {
    // Update the state
    this.setState({ selectedFile: event.target.files[0] });
  };
  onCheckFile () {
    fetch("http://localhost:5000/checkPDF", {
      method: "get",
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        console.log(data);

        console.log("bad", data["bad"][0]);
        
        console.log("good", data["good"][0]);
        this.setState({ goodData: data["good"][0] });
        this.setState({ badData: data["bad"][0] });
        
      });
  };
  // On file upload (click the upload button)
  onFileUpload = async () => {
    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    // formData.append(
    //   "myFile",
    //   this.state.selectedFile,
    //   this.state.selectedFile.name
    // );
    formData.append("file", this.state.selectedFile);
    // Details of the uploaded file
    console.log(this.state.selectedFile);

    // Request made to the backend api
    // Send formData object
    // axios.post("http://localhost:5000/uploads", formData);
    const res = await axios.post("http://localhost:5000/uploads", formData);
    console.log("Response ", res.data);
    if (res.status === 200) {
      console.log("data");
      console.log(res.data);
    } else {
      console.log("error");
    }
  };

  // File content to be displayed after
  // file upload is complete
  fileData = () => {
    if (this.state.selectedFile) {
      return (
        <div>
          <h2>File Details:</h2>

          <p>File Name: {this.state.selectedFile.name}</p>

          <p>File Type: {this.state.selectedFile.type}</p>

          <p>
            Last Modified:{" "}
            {this.state.selectedFile.lastModifiedDate.toDateString()}
          </p>
        </div>
      );
    } else {
      return (
        <div>
          <br />
          <h4>Choose before Pressing the Upload button</h4>
        </div>
      );
    }
  };

  render() {
    return (
      <div>
        <h1>Verify your offer letter</h1>

        <div>
          <input type="file" onChange={this.onFileChange} />
          <button onClick={this.onFileUpload}>Upload!</button>
        </div>

        <button onClick={this.onCheckFile}>Check the File</button>
        {this.fileData()}
        {this.state.goodData ? (
          <div>
            <p>Good data:{this.state.goodData}</p>
            <p>Bad data:{this.state.badData}</p>
          </div>
        ) : null}
        <button onClick={this.onResult}>Check Full Result</button>
      </div>
    );
  }
}

render(<App />, document.getElementById("app"));
