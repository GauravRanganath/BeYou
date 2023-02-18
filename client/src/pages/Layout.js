import { Outlet, Link } from "react-router-dom";
import ColorSchemesExample from "../components/Navbar";

const Layout = () => {
  return (
    <>
      <ColorSchemesExample />
      <Outlet />
    </>
  );
};

export default Layout;
