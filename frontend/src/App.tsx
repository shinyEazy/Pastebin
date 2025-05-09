import { Outlet } from "react-router-dom";
import Layout from "./components/Layout/Layout";

const App = () => {
  return (
    <Layout>
      <Outlet />
    </Layout>
  );
};

export default App;
