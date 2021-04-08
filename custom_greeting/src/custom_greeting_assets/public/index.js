import { render } from "react-dom";
import axios from "axios";
import * as React from "react";
//import logo from "./logo.png";
import "./style.css";

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedFile: null,
      loading: false,
      goodData: "good",
      badData: "bad",
    };

    //this.onCheckFile = this.onCheckFile.bind(this);
  }

  onResult = () => {
    window.open("http://localhost:5000/checkPDF");
  };
  // On file select (from the pop up)
  onFileChange = (event) => {
    // Update the state
    this.setState({ selectedFile: event.target.files[0] });
  };

  // On file upload (click the upload button)
  onFileUpload = async () => {
    this.setState({ uploading: true });
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

    const response = await axios.get("http://localhost:5000/checkPDF");
    console.log("res data", response.data);
    console.log("good", response.data["good"][0]);
    console.log("good", response.data["bad"][0]);
    this.setState({ goodData: response.data["good"][0] });
    this.setState({ badData: response.data["bad"][0] });
    this.setState({ uploading: false });
    /* fetch("http://localhost:5000/checkPDF", {
      method: "get",
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        console.log(data);

        console.log("bad", data["bad"][0]);

        console.log("good", data["good"][0]);
        this.setState({ goodData: data });
       
      }); */
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
        <div className="modal-header">
          <h1 className="logo">
            <img
              className="logo-icon"
              src={
                "data:image/svg+xml;charset=UTF-8,%3csvg aria-hidden='true' focusable='false' data-prefix='fas' data-icon='file-signature' class='svg-inline--fa fa-file-signature fa-w-18' role='img' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 576 512'%3e%3cpath fill='currentColor' d='M218.17 424.14c-2.95-5.92-8.09-6.52-10.17-6.52s-7.22.59-10.02 6.19l-7.67 15.34c-6.37 12.78-25.03 11.37-29.48-2.09L144 386.59l-10.61 31.88c-5.89 17.66-22.38 29.53-41 29.53H80c-8.84 0-16-7.16-16-16s7.16-16 16-16h12.39c4.83 0 9.11-3.08 10.64-7.66l18.19-54.64c3.3-9.81 12.44-16.41 22.78-16.41s19.48 6.59 22.77 16.41l13.88 41.64c19.75-16.19 54.06-9.7 66 14.16 1.89 3.78 5.49 5.95 9.36 6.26v-82.12l128-127.09V160H248c-13.2 0-24-10.8-24-24V0H24C10.7 0 0 10.7 0 24v464c0 13.3 10.7 24 24 24h336c13.3 0 24-10.7 24-24v-40l-128-.11c-16.12-.31-30.58-9.28-37.83-23.75zM384 121.9c0-6.3-2.5-12.4-7-16.9L279.1 7c-4.5-4.5-10.6-7-17-7H256v128h128v-6.1zm-96 225.06V416h68.99l161.68-162.78-67.88-67.88L288 346.96zm280.54-179.63l-31.87-31.87c-9.94-9.94-26.07-9.94-36.01 0l-27.25 27.25 67.88 67.88 27.25-27.25c9.95-9.94 9.95-26.07 0-36.01z'%3e%3c/path%3e%3c/svg%3e"
              }
            />
            DocVerifier
          </h1>
        </div>
        <p id="loading-text"></p>
        <div className="modal-content" id="description">
          <p>
            {" "}
            Be Honest! How many times have you clicked "Accept Terms and
            Conditions" without reading them? <br></br>A lot of times, right?
            But not anymore.
          </p>
          <p>
            DocVerifier is a tool to summarize and report sketchy policies and
            flaws in long agreements/texts.{" "}
          </p>
        </div>
        <div className="upload">
          <input type="file" onChange={this.onFileChange} />
          <button onClick={this.onFileUpload}>Check the file</button>
          <div>
            {/* <button>Check the File</button> */}
            <br />
            {/* <h4 id="message-1">Choose before Pressing the Upload button</h4> */}
            {/* {this.fileData()} */}
            <center></center>
            {this.state.uploading ? (
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
                className="loader"
              ></div>
            ) : null}
            {this.state.goodData ? (
              <div>
                <h2> Output : </h2>
                <div class="output">
                  <p>
                    <b>Good data: </b>
                    {this.state.goodData}
                  </p>
                  <p>
                    <b>Bad data:</b> {this.state.badData}
                  </p>
                </div>
              </div>
            ) : null}
            <button id="resultButton" onClick={this.onResult}>
              See Full Result
            </button>
          </div>
        </div>
      </div>
    );
  }
}

render(<App />, document.getElementById("app"));
