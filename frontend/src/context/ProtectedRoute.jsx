import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { token } = useContext(AuthContext);

  if (!token) {
    // If no token, redirect to home
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;