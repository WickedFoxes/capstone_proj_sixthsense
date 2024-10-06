import "./App.css";
import { Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import SignUp from "./components/SignUp";
import Header from "./components/Header";
import Project from "./components/Project";
import Menubar from "./components/Menubar";
import UrlInput from "./components/UrlInput";
import Url from "./components/Url";
import ListGroup from "react-bootstrap/ListGroup";

function App() {
  return (
    <>
      <div className="App">
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Login />
              </>
            }
          />
          <Route
            path="/signup"
            element={
              <>
                <SignUp />
              </>
            }
          />
          <Route
            path="/main"
            element={
              <>
                <Header />
                <Menubar />
                <Project />
              </>
            }
          />
          <Route
            path="/project/:projectId"
            element={
              <>
                <Header />
                <UrlInput />
                <ListGroup as="ol" numbered>
                  <Url />
                </ListGroup>
              </>
            }
          />
        </Routes>
      </div>
    </>
  );
}

export default App;
