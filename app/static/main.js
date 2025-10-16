const form = document.getElementById('accForm');
const list = document.getElementById('accountsList');

async function loadAccounts(){
  const res = await fetch('/api/accounts');
  const data = await res.json();
  list.innerHTML = data.map(a => `<li>${a.id}: ${a.name} — ${a.email} — ₹${a.balance}</li>`).join('');
}

form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const formData = new FormData(form);
  const payload = {
    name: formData.get('name'),
    email: formData.get('email'),
    phone: formData.get('phone'),
    dob: formData.get('dob'),
    balance: parseFloat(formData.get('balance') || 0)
  };
  const res = await fetch('/api/accounts', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });
  if(res.ok){
    alert('Account created');
    form.reset();
    loadAccounts();
  } else {
    const err = await res.json();
    alert('Error: ' + (err.message || JSON.stringify(err)));
  }
});

window.onload = loadAccounts;
