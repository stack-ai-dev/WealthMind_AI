/**
 * WealthMind AI - Home Page
 *
 * BEGINNER NOTES:
 * - All CSS is inside the "styles" object at the BOTTOM of this file
 * - Your original move() logic is kept exactly the same
 * - Every section has a comment explaining what it does
 */
      
import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Home() {
  const navigate = useNavigate();
  const { token } = useContext(AuthContext);

  // YOUR ORIGINAL LOGIC — not changed at all
  const move = () => {
    if (token) {
      navigate("/Chat");
    } else {
      navigate("/Login");
    }
  };

  // List of feature cards to show on the page
  // To add a new card — just add a new object { icon, title, text } here
  const features = [
    { icon: "🧠", title: "AI Profile Analysis",  text: "Tells you your investor type based on your age, income and goals." },
    { icon: "📊", title: "ML Risk Scoring",       text: "A trained model gives your portfolio a risk score from 0 to 100." },
    { icon: "📈", title: "Live Market Data",       text: "Real prices for S&P 500, Bitcoin, and more — updated live." },
    { icon: "💬", title: "Chat Advisor",           text: "Ask follow-up questions. The AI remembers your strategy." },
    { icon: "🔍", title: "RAG Knowledge Base",     text: "Answers are backed by real investment research, not just guesses." },
    { icon: "📉", title: "Growth Simulation",      text: "See how your money grows year by year using compound interest." },
  ];

  // The 8 pipeline steps shown in the "How It Works" section
  const steps = [
    "1. Profile Agent",
    "2. RAG Retrieve",
    "3. Market Data",
    "4. Strategy Agent",
    "5. Risk Engine",
    "6. Simulation",
    "7. Advisor Agent",
    "8. Memory Store",
  ];
 
  return (
    <div style={styles.page}>

      {/* NAVBAR */}
      <div style={styles.navbar}>

        {/* Logo on the left side */}
        <div style={styles.logo}>
          <div style={styles.logoIcon}>💰</div>
          <span style={styles.logoText}>WealthMind AI 💰</span>
        </div>

        {/* Button on the right — calls your move() function */}
        <button style={styles.navButton} onClick={move}>
          {token ? "Go to Chat" : "Get Started"}
        </button>

      </div>


      {/*HERO (big welcome section in the middle)*/}
      <div style={styles.hero}>

        {/* Small pill label at the top */}
        <div style={styles.badge}>
          AI · Machine Learning · Live Data
        </div>

        {/* Big heading */}
        <h1 style={styles.heroTitle}>
          Your Personal AI<br />
          <span style={styles.greenText}>Investment Advisor</span>
        </h1>

        {/* Description paragraph */}
        <p style={styles.heroSubtitle}>
          WealthMind looks at your financial profile, scores your risk
          using a real ML model, and builds a personalized investment plan
          — all in one click.
        </p>

        {/* Main CTA button — calls your move() function */}
        <button style={styles.bigButton} onClick={move}>
          {token ? "Continue to Chat →" : "Get Started Free →"}
        </button>

      </div>


      {/*FEATURES SECTION */}
      <div style={styles.section}>

        <h2 style={styles.sectionTitle}>What WealthMind Does</h2>
        <p style={styles.sectionSub}>
          Six powerful features working together in one AI pipeline.
        </p>

        {/* Loop through the features array and render a card for each */}
        <div style={styles.grid}>
          {features.map((item, index) => (
            <div key={index} style={styles.card}>
              <div style={styles.cardIcon}>{item.icon}</div>
              <h3 style={styles.cardTitle}>{item.title}</h3>
              <p style={styles.cardText}>{item.text}</p>
            </div>
          ))}
        </div>

      </div>


      {/*HOW IT WORKS SECTION */}
      <div style={styles.section}>

        <h2 style={styles.sectionTitle}>How It Works</h2>
        <p style={styles.sectionSub}>
          8 AI steps run one after another to build your strategy.
        </p>

        {/* Loop through steps and show a box + arrow for each */}
        <div style={styles.pipeline}>
          {steps.map((step, index) => (
            <div key={index} style={styles.pipelineItem}>
              <div style={styles.pipelineBox}>{step}</div>
              {/* Show → arrow after every step EXCEPT the last one */}
              {index < steps.length - 1 && (
                <span style={styles.arrow}>→</span>
              )}
            </div>
          ))}
        </div>

      </div>

      {/*FOOTER*/}
      <div style={styles.footer}>
        WealthMind AI — Built with FastAPI · LangGraph · React
      </div>

    </div>
  );
}



const styles = {

  // The full page wrapper
  page: {
    minHeight: "100vh",
    backgroundColor: "#0d1117",     // very dark navy background
    color: "#f0f4ff",               // light text by default
    fontFamily: "'Segoe UI', sans-serif",
  },

  // Navbar 
  navbar: {
    display: "flex",
    justifyContent: "space-between", // pushes logo left and button right
    alignItems: "center",
    padding: "16px 32px",
    borderBottom: "1px solid #1f2937",
  },

  logo: {
    display: "flex",
    alignItems: "center",
    gap: "10px",                     // space between icon and text
  },

  logoIcon: {
    width: "36px",
    height: "36px",
    borderRadius: "8px",
    backgroundColor: "#0077ff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#ffffff",
    fontWeight: "bold",
    fontSize: "16px",
  },

  logoText: {
    fontSize: "16px",
    fontWeight: "700",
    color: "#f0f4ff",
  },

  navButton: {
    backgroundColor: "#0077ff",
    color: "#ffffff",
    border: "none",
    borderRadius: "8px",
    padding: "9px 20px",
    fontSize: "14px",
    fontWeight: "600",
    cursor: "pointer",
  },

  //Hero 
  hero: {
    textAlign: "center",
    padding: "80px 24px 60px",
    maxWidth: "620px",
    margin: "0 auto",               // centers the block horizontally
  },

  badge: {
    display: "inline-block",
    backgroundColor: "rgba(0,201,167,0.12)",
    border: "1px solid rgba(0,201,167,0.3)",
    borderRadius: "20px",
    padding: "5px 14px",
    fontSize: "12px",
    color: "#00c9a7",
    fontWeight: "600",
    marginBottom: "24px",
  },

  heroTitle: {
    fontSize: "46px",
    fontWeight: "800",
    lineHeight: "1.2",
    margin: "0 0 16px",
    color: "#f0f4ff",
  },

  greenText: {
    color: "#00c9a7",               // teal/green accent color
  },

  heroSubtitle: {
    fontSize: "16px",
    color: "#9ca3b8",               // muted grey text
    lineHeight: "1.7",
    marginBottom: "32px",
  },

  bigButton: {
    backgroundColor: "#0077ff",
    color: "#ffffff",
    border: "none",
    borderRadius: "10px",
    padding: "14px 32px",
    fontSize: "16px",
    fontWeight: "700",
    cursor: "pointer",
  },

  // Section (shared by Features and Pipeline) 
  section: {
    maxWidth: "960px",
    margin: "0 auto",
    padding: "50px 24px",
  },

  sectionTitle: {
    textAlign: "center",
    fontSize: "28px",
    fontWeight: "800",
    color: "#f0f4ff",
    margin: "0 0 8px",
  },

  sectionSub: {
    textAlign: "center",
    fontSize: "15px",
    color: "#6b7280",
    marginBottom: "36px",
  },

  // Feature cards 
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)", // 3 equal columns
    gap: "16px",
  },

  card: {
    backgroundColor: "#161b22",
    border: "1px solid #1f2937",
    borderRadius: "12px",
    padding: "20px",
  },

  cardIcon: {
    fontSize: "28px",
    marginBottom: "10px",
  },

  cardTitle: {
    fontSize: "15px",
    fontWeight: "700",
    color: "#f0f4ff",
    margin: "0 0 6px",
  },

  cardText: {
    fontSize: "13px",
    color: "#6b7280",
    lineHeight: "1.6",
    margin: "0",
  },

  // Pipeline 
  pipeline: {
    display: "flex",
    flexWrap: "wrap",               // wrap to next line on small screens
    justifyContent: "center",
    alignItems: "center",
    gap: "6px",
  },

  pipelineItem: {
    display: "flex",
    alignItems: "center",
    gap: "6px",
  },

  pipelineBox: {
    backgroundColor: "rgba(0,119,255,0.1)",
    border: "1px solid rgba(0,119,255,0.25)",
    borderRadius: "8px",
    padding: "8px 12px",
    fontSize: "12px",
    color: "#60a5fa",
    fontWeight: "600",
  },

  arrow: {
    fontSize: "14px",
    color: "#374151",
  },

  //Footer 
  footer: {
    textAlign: "center",
    padding: "20px",
    borderTop: "1px solid #1f2937",
    fontSize: "12px",
    color: "#374151",
  },

};

export default Home;
