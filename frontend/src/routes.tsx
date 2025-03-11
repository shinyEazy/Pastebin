import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import Home from "./pages/Home";
import CreatePaste from "./pages/CreatePaste";
import ViewPaste from "./pages/ViewPaste";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "create",
        element: <CreatePaste />,
      },
      {
        path: "paste/:id",
        element: <ViewPaste />,
        loader: async ({ params }) => {
          if (!params.id) throw new Error("Paste ID is required");
          return { pasteId: params.id };
        },
      },
    ],
  },
]);

export default router;
