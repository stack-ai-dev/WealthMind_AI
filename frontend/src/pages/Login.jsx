import { useState, useContext } from "react";
import API from "../api/axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await API.post("/auth/login", form);
      login(res.data.access_token);
      navigate("/chat");
      alert("Login Successfully");
    } catch (err) {
      alert("Login failed");
    }
  };

  const goToRegister = () => {
    navigate("/register");
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Login</h1>

        <input
          placeholder="Email"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          style={styles.input}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          style={styles.input}
        />

        <div style={styles.buttonGroup}>
          <button onClick={handleLogin} style={styles.button}>
            Login
          </button>
          <button onClick={goToRegister} style={styles.secondaryButton}>
            Register
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    background: "linear-gradient(135deg, #141e30, #243b55)",
  },
  card: {
    background: "#fff",
    padding: "40px",
    borderRadius: "12px",
    width: "350px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.2)",
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
    color: "#141e30",
  },
  input: {
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    fontSize: "14px",
  },
  buttonGroup: {
    display: "flex",
    justifyContent: "space-between",
    gap: "10px",
    marginTop: "10px",
  },
  button: {
    flex: 1,
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#4a90e2",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "background 0.3s ease",
  },
  secondaryButton: {
    flex: 1,
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#e74c3c",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "background 0.3s ease",
  },
};

export default Login;