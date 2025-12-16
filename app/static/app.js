function getToken() {
  return localStorage.getItem("token");
}
function setToken(t) {
  if (t) localStorage.setItem("token", t);
}
function clearToken() {
  localStorage.removeItem("token");
}
function authHeaders() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}
function show(el, msg, ok=false){
  if(!el) return;
  el.style.color = ok ? "#065f46" : "#b91c1c";
  el.textContent = msg || "";
}

async function api(path, opts={}) {
  const res = await fetch(path, opts);
  let data = null;
  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) data = await res.json();
  else data = await res.text();
  if (!res.ok) {
    const detail = (data && data.detail) ? data.detail : (typeof data === "string" ? data : "Request failed");
    throw new Error(detail);
  }
  return data;
}

async function handleRegister() {
  const u = document.getElementById("username")?.value?.trim();
  const e = document.getElementById("email")?.value?.trim();
  const p = document.getElementById("password")?.value;
  const msg = document.getElementById("msg");
  if (!u || !e || !p) return show(msg, "Fill all fields");
  if (p.length < 8) return show(msg, "Password must be at least 8 characters");
  try{
    const data = await api("/api/auth/register", {
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({username:u, email:e, password:p})
    });
    setToken(data.access_token);
    show(msg, "Registered! Redirecting...", true);
    window.location.href = "/";
  }catch(err){ show(msg, err.message); }
}

async function handleLogin() {
  const u = document.getElementById("username")?.value?.trim();
  const p = document.getElementById("password")?.value;
  const msg = document.getElementById("msg");
  if (!u || !p) return show(msg, "Enter username and password");
  const form = new URLSearchParams();
  form.append("username", u);
  form.append("password", p);
  try{
    const data = await api("/api/auth/token", {
      method:"POST",
      headers:{ "Content-Type":"application/x-www-form-urlencoded" },
      body: form.toString()
    });
    setToken(data.access_token);
    show(msg, "Logged in! Redirecting...", true);
    window.location.href = "/";
  }catch(err){ show(msg, err.message); }
}

async function loadProfile() {
  const msg = document.getElementById("profileMsg");
  try{
    const me = await api("/api/profile", { headers: { ...authHeaders() } });
    document.getElementById("p_username").value = me.username;
    document.getElementById("p_email").value = me.email;
    show(msg, "");
  }catch(err){ show(msg, "Please login first"); }
}

async function saveProfile() {
  const u = document.getElementById("p_username")?.value?.trim();
  const e = document.getElementById("p_email")?.value?.trim();
  const msg = document.getElementById("profileMsg");
  try{
    const updated = await api("/api/profile", {
      method:"PUT",
      headers:{ "Content-Type":"application/json", ...authHeaders() },
      body: JSON.stringify({ username: u || null, email: e || null })
    });
    show(msg, "Saved!", true);
  }catch(err){ show(msg, err.message); }
}

async function changePw() {
  const cur = document.getElementById("cur_pw")?.value;
  const nw = document.getElementById("new_pw")?.value;
  const msg = document.getElementById("pwMsg");
  if(!cur || !nw) return show(msg, "Fill both password fields");
  if(nw.length < 8) return show(msg, "New password must be at least 8 characters");
  try{
    await api("/api/profile/change-password", {
      method:"POST",
      headers:{ "Content-Type":"application/json", ...authHeaders() },
      body: JSON.stringify({ current_password: cur, new_password: nw })
    });
    show(msg, "Password changed. Please login again.", true);
    clearToken();
  }catch(err){ show(msg, err.message); }
}

async function doCalc() {
  const a = parseFloat(document.getElementById("a")?.value);
  const b = parseFloat(document.getElementById("b")?.value);
  const op = document.getElementById("op")?.value;
  const msg = document.getElementById("calcMsg");
  try{
    const out = await api("/api/calculations", {
      method:"POST",
      headers:{ "Content-Type":"application/json", ...authHeaders() },
      body: JSON.stringify({ a, b, op })
    });
    show(msg, `Result: ${out.result}`, true);
    await refreshHistory();
    await refreshStats();
  }catch(err){ show(msg, err.message); }
}

async function refreshHistory(){
  const body = document.getElementById("histBody");
  if(!body) return;
  body.innerHTML = "";
  try{
    const rows = await api("/api/calculations", { headers: { ...authHeaders() }});
    for(const r of rows){
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${r.id}</td><td>${r.a}</td><td>${r.b}</td><td>${r.op}</td><td>${r.result}</td>`;
      body.appendChild(tr);
    }
  }catch(err){
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="5">Login to see history</td>`;
    body.appendChild(tr);
  }
}

async function refreshStats(){
  const box = document.getElementById("statsBox");
  if(!box) return;
  try{
    const s = await api("/api/reports/stats", { headers: { ...authHeaders() }});
    box.textContent = JSON.stringify(s, null, 2);
  }catch(err){
    box.textContent = "Login to see stats";
  }
}

function wireNav(){
  const logout = document.getElementById("navLogout");
  if(logout){
    logout.addEventListener("click", () => { clearToken(); window.location.href="/login"; });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  wireNav();
  document.getElementById("btnRegister")?.addEventListener("click", handleRegister);
  document.getElementById("btnLogin")?.addEventListener("click", handleLogin);
  document.getElementById("btnProfileSave")?.addEventListener("click", saveProfile);
  document.getElementById("btnChangePw")?.addEventListener("click", changePw);
  document.getElementById("btnCalc")?.addEventListener("click", doCalc);
  document.getElementById("btnHistory")?.addEventListener("click", refreshHistory);
  document.getElementById("btnStats")?.addEventListener("click", refreshStats);

  if (window.location.pathname === "/profile") loadProfile();
  if (window.location.pathname === "/") { refreshHistory(); refreshStats(); }
});
