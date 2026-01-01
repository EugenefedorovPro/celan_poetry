import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import "./index.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "./components/layout/Layout";
import { Login } from "./pages/Login";
import { Logout } from "./pages/Logout";
import { Signup } from "./pages/Signup";
import Collection from "./pages/Collection";
import { TocVerse } from "./pages/TocVerse";
import { Verse } from "./pages/Verse";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Collection />} />
          <Route path="login" element={<Login />} />
          <Route path="logout" element={<Logout />} />
          <Route path="signup" element={<Signup />} />
          <Route path="collections/:collectionId/toc" element={<TocVerse />} />
          <Route path="verse/:verseId/" element={<Verse />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
