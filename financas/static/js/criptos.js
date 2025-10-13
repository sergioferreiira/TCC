// financas/static/js/criptos.js
(function () {
  const btn = document.getElementById("btn-checar");
  const tbl = document.getElementById("tabela-criptos").querySelector("tbody");
  const statusMsg = document.getElementById("status-msg");
  const symbolsInput = document.getElementById("symbols");
  const convertInput = document.getElementById("convert");

  async function atualizar() {
    const symbols = (symbolsInput.value || "BTC,ETH").trim();
    const convert = (convertInput.value || "USD").trim();

    const url = `/criptos/atualizar/?symbols=${encodeURIComponent(symbols)}&convert=${encodeURIComponent(convert)}`;

    btn.disabled = true;
    const oldText = btn.innerText;
    btn.innerText = "Buscando...";
    statusMsg.innerText = "";

    try {
      const resp = await fetch(url, { method: "GET", headers: { "Accept": "application/json" } });
      const data = await resp.json();

      if (!resp.ok || !data.ok) {
        throw new Error(data && data.error ? data.error : `Erro HTTP ${resp.status}`);
      }

      (data.saved || []).forEach(item => {
        const tr = document.createElement("tr");
        const dt = new Date(item.data_consulta);
        const dtDisplay = dt.toLocaleString();

        tr.innerHTML = `
          <td data-iso="${item.data_consulta}">${dtDisplay}</td>
          <td>${item.simbolo}</td>
          <td>${item.nome}</td>
          <td>${Number(item.preco).toFixed(8)}</td>
          <td>${Number(item.variacao_24h) >= 0
            ? `<span class="text-success">+${Number(item.variacao_24h).toFixed(2)}%</span>`
            : `<span class="text-danger">${Number(item.variacao_24h).toFixed(2)}%</span>`
          }</td>
          <td>${item.moeda_fiat}</td>
        `;
        // adiciona no topo
        if (tbl.firstChild) {
          tbl.insertBefore(tr, tbl.firstChild);
        } else {
          tbl.appendChild(tr);
        }
      });

      statusMsg.innerText = `Atualizado em ${new Date(data.updated_at).toLocaleString()} (${data.count} registro(s))`;
    } catch (err) {
      console.error(err);
      statusMsg.innerText = `Erro: ${err.message || err}`;
      statusMsg.classList.add("text-danger");
    } finally {
      btn.disabled = false;
      btn.innerText = oldText;
      setTimeout(() => {
        statusMsg.classList.remove("text-danger");
      }, 4000);
    }
  }

  if (btn) btn.addEventListener("click", atualizar);
})();
