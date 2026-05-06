import React, { useState, useContext } from "react";
import API from "../api/axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Chatbot = () => {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [result, setResult]   = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    age: "",
    income: "",
    savings: "",
    risk_tolerance: "medium",
    goal: "",
    time_horizon: "",
    monthly_contribution: "",
    explain_mode: "beginner",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSend = async () => {
    setLoading(true);
    const payload = {
      profile: {
        name:           formData.name,
        age:            Number(formData.age),
        income:         Number(formData.income),
        savings:        Number(formData.savings),
        risk_tolerance: formData.risk_tolerance,
        goal:           formData.goal,
        time_horizon:   Number(formData.time_horizon),
      },
      session_id:           "default",
      monthly_contribution: Number(formData.monthly_contribution),
      explain_mode:         formData.explain_mode,
    };
    try {
      const res = await API.post("/ai/analyze", payload);
      setResult(res.data);
      alert("Analysis completed successfully");
    } catch (err) {
      console.error(err);
      alert("Analysis failed");
    }
    setLoading(false);
  };

  const handlelogout = () => {
    logout();
    navigate("/");
  };

  const getRiskColor = (label) => {
    if (label === "Low")    return "#16a34a";
    if (label === "Medium") return "#d97706";
    if (label === "High")   return "#ef4444";
    return "#64748b";
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>💰 AI Wealth Advisor</h2>

        <div style={styles.splitLayout}>

          {/* Left — form */}
          <div style={styles.form}>
            <input name="name" placeholder="👤 Name" onChange={handleChange} style={styles.input} />
            <input name="age"  placeholder="🎂 Age" onChange={handleChange} style={styles.input} />
            <input name="income" placeholder="💵 Income" onChange={handleChange} style={styles.input} />
            <input name="savings"  placeholder="🏦 Savings" onChange={handleChange} style={styles.input} />
            <input name="goal"  placeholder="🎯 Goal (house, car...)"onChange={handleChange} style={styles.input} />
            <input name="time_horizon" placeholder="📅 Years"  onChange={handleChange} style={styles.input} />
            <input name="monthly_contribution" placeholder="📈 Monthly Investment" onChange={handleChange} style={styles.input} />

            <select name="risk_tolerance" value={formData.risk_tolerance} onChange={handleChange} style={styles.input}>
              <option value="low">Low Risk</option>
              <option value="medium">Medium Risk</option>
              <option value="high">High Risk</option>
            </select>

            <select name="explain_mode" value={formData.explain_mode} onChange={handleChange} style={styles.input}>
              <option value="beginner">Beginner Mode</option>
              <option value="investor">Investor Mode</option>
            </select>

            <button onClick={handleSend} style={styles.analyzeButton}>
              {loading ? "⏳ Analyzing..." : "🔍 Analyze"}
            </button>
            <button onClick={handlelogout} style={styles.logoutButton}>
              🚪 Logout
            </button>
          </div>

          {/* Right — results */}
          <div style={styles.responseBox}>

            {!result && (
              <p style={styles.placeholder}>📊 Results will appear here...</p>
            )}

            {result && (
              <div>
                <p style={styles.sectionLabel}>Profile Type</p>
                <p style={styles.profileType}>{result.strategy.profile_type}</p>

                <p style={styles.sectionLabel}>Risk Score</p>
                <p style={{ ...styles.riskScore, color: getRiskColor(result.strategy.risk_label) }}>
                  {result.strategy.risk_score} / 100 — {result.strategy.risk_label}
                </p>

                <p style={styles.sectionLabel}>Allocation</p>
                <ul style={styles.list}>
                  {Object.entries(result.strategy.allocation).map(([key, value]) => (
                    <li key={key} style={styles.listItem}>
                      <span style={styles.assetName}>{key}</span>
                      <span style={styles.assetValue}>{value}%</span>
                    </li>
                  ))}
                </ul>

                <p style={styles.sectionLabel}>Key Numbers</p>
                <div style={styles.numbersRow}>
                  <div style={styles.numberBox}>
                    <p style={styles.numberLabel}>Final Value</p>
                    <p style={styles.numberValue}>${result.simulation.final_value.toLocaleString()}</p>
                  </div>
                  <div style={styles.numberBox}>
                    <p style={styles.numberLabel}>Total Gain</p>
                    <p style={styles.numberValue}>+${result.simulation.total_gain.toLocaleString()}</p>
                  </div>
                  <div style={styles.numberBox}>
                    <p style={styles.numberLabel}>Return / yr</p>
                    <p style={styles.numberValue}>{result.strategy.expected_annual_return}%</p>
                  </div>
                </div>

                <p style={styles.sectionLabel}>Recommendations</p>
                <ul style={styles.list}>
                  {result.strategy.recommendations.map((rec, index) => (
                    <li key={index} style={styles.recItem}>{rec}</li>
                  ))}
                </ul>

                <p style={styles.sectionLabel}>AI Explanation</p>
                <p style={styles.explanation}>{result.strategy.explanation}</p>

                <p style={styles.marketSummary}>{result.market_summary}</p>
              </div>
            )}

          </div>
        </div>
      </div>
    </div>
  );
};




const styles = {

  
  container: {
    display: "flex",              // use flexbox to center the card
    justifyContent: "center",     // center horizontally
    alignItems: "center",         // center vertically
    height: "100vh",              // 100vh = full screen height
    background: "linear-gradient(to bottom right, #0f172a, #334155)",
  
  },

  card: {
    background: "#ffffff",        // white background
    padding: "25px",              // space inside the card on all sides
    borderRadius: "15px",         // rounded corners
    width: "900px",               // fixed width
    boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
    //          ^ shadow: 0 left/right, 10px down, 30px blur, 20% black
    display: "flex",              // children stack vertically
    flexDirection: "column",      // stack top to bottom
    gap: "20px",                  // space between title and split layout
  },


  title: {
    textAlign: "center",          // center the text horizontally
    color: "#1e293b",             // dark navy text
  },

  
  splitLayout: {
    display: "flex",              // side by side (flex default is row)
    gap: "20px",                  // space between left and right columns
  },

  
  form: {
    display: "flex",              // stack inputs vertically
    flexDirection: "column",      // top to bottom
    gap: "10px",                  // space between each input
    flex: "1",                    // take up 50% of available width
  },

  
  input: {
    padding: "10px",              // space inside the input box
    borderRadius: "8px",          // slightly rounded corners
    border: "1px solid #ccc",     // thin grey border
    fontSize: "14px",             // text size inside the box
    outline: "none",              // remove default blue outline on click
  },

 
  analyzeButton: {
    background: "#22c55e",        // green background
    color: "white",               // white text
    padding: "10px",              // space inside button
    border: "none",               // no border
    borderRadius: "10px",         // rounded corners
    cursor: "pointer",            // hand cursor when hovering
    fontWeight: "bold",           // bold text
  },

  
  logoutButton: {
    background: "#ef4444",        // red background
    color: "white",
    padding: "10px",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
  },

  
  responseBox: {
  flex: "1",
  border: "1px solid #ddd",
  padding: "15px",
  borderRadius: "10px",
  background: "#f8fafc",
  height: "488px",      //  FIXED HEIGHT (important)
  overflowY: "auto",    // enables vertical scroll
},

  
 
  placeholder: {
    color: "#94a3b8",             // light grey text
    fontSize: "14px",
    textAlign: "center",
    marginTop: "80px",            // push it down to the middle of the box
  },

 
  
  sectionLabel: {
    fontSize: "11px",
    color: "#64748b",             // medium grey
    textTransform: "uppercase",   // makes text ALL CAPS automatically
    letterSpacing: "0.8px",       // small space between each letter
    margin: "14px 0 4px",         // 14px top gap, 4px bottom gap
  },

  
  profileType: {
    color: "#1e293b",             // dark navy
    fontSize: "16px",
    fontWeight: "700",            // 700 = bold
    margin: "0",                  // remove default paragraph spacing
  },

  
  riskScore: {
    fontSize: "15px",
    fontWeight: "700",
    margin: "0",
  },

 
  list: {
    margin: "0",
    padding: "0",
    listStyle: "none",            // remove default bullet points
  },

 

  listItem: {
    display: "flex",
    justifyContent: "space-between", // name on left, % on right
    padding: "5px 0",
    borderBottom: "1px solid #e2e8f0", // thin line under each row
    fontSize: "13px",
  },
  assetName: {
    color: "#475569",
    textTransform: "capitalize",  // makes "stocks" → "Stocks"
  },
  assetValue: {
    color: "#0077ff",             // blue percentage number
    fontWeight: "700",
  },

  
  numbersRow: {
    display: "flex",              // side by side
    gap: "8px",                   // space between boxes
  },
  numberBox: {
    flex: "1",                    // each box gets equal width
    backgroundColor: "#f1f5f9",   // light grey background
    border: "1px solid #e2e8f0",
    borderRadius: "8px",
    padding: "10px",
    textAlign: "center",          // center text inside box
  },
  numberLabel: {
    fontSize: "10px",
    color: "#64748b",
    margin: "0 0 4px",            // small gap between label and value
    textTransform: "uppercase",
  },
  numberValue: {
    fontSize: "14px",
    fontWeight: "700",
    color: "#16a34a",             // green number
    margin: "0",
  },

  
  recItem: {
    color: "#475569",
    fontSize: "13px",
    padding: "4px 0",
    listStyle: "disc",            // show bullet point
    listStylePosition: "inside",  // bullet point inside the box
  },

  
  explanation: {
    color: "#475569",
    fontSize: "13px",
    lineHeight: "1.7",            // space between lines (1.7 = relaxed)
    margin: "0",
    backgroundColor: "#f1f5f9",
    border: "1px solid #e2e8f0",
    borderRadius: "8px",
    padding: "12px",
  },

 
  marketSummary: {
    color: "#94a3b8",             // light grey
    fontSize: "11px",
    marginTop: "14px",
    paddingTop: "10px",
    borderTop: "1px solid #e2e8f0", // thin line above it
  },

};

export default Chatbot;


