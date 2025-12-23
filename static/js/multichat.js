(() => {
  const STORAGE_KEY = 'multichat_state';

  const elColumns = document.getElementById('columns');
  const elAdd = document.getElementById('addColumn');
  let globalMenu;

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const s = JSON.parse(raw);
        if (Array.isArray(s.columns) && s.columns.length >= 0) {
          // normalize widths sum to 100
          const sum = s.columns.reduce((acc, c) => acc + (Number(c.width) || 0), 0);
          if (sum > 0) s.columns.forEach(c => c.width = (Number(c.width) || 0) * (100 / sum));
          return s;
        }
      }
    } catch {}
    // default: 3 empty columns split equally
    return {
      columns: [
        { url: '', width: 33.3333 },
        { url: '', width: 33.3334 },
        { url: '', width: 33.3333 },
      ],
    };
  }

  function saveState(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch {}
  }

  let state = loadState();

  function setEqualWidths() {
    const n = state.columns.length;
    if (n === 0) return;
    const w = 100 / n;
    state.columns.forEach((c, i) => c.width = i === n - 1 ? (100 - w * (n - 1)) : w);
  }

  function render() {
    elColumns.innerHTML = '';
    state.columns.forEach((col, index) => {
      const colEl = createColumnElement(col, index);
      elColumns.appendChild(colEl);
    });
  }

  function createColumnElement(col, index) {
    const colEl = document.createElement('div');
    colEl.className = 'column' + (col.url ? ' has-url' : '');
    colEl.style.flexBasis = `${col.width}%`;
    colEl.dataset.index = String(index);

    const content = document.createElement('div');
    content.className = 'column-content';

    // input area
    const inputArea = document.createElement('div');
    inputArea.className = 'input-area';
    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Enlace (YouTube/Twitch/URL)...';
    input.value = col.url || '';
    const showBtn = document.createElement('button');
    showBtn.className = 'show-btn';
    showBtn.textContent = 'Mostrar chat';
    inputArea.appendChild(input);
    inputArea.appendChild(showBtn);

    // iframe
    const iframe = document.createElement('iframe');
    iframe.className = 'chat-frame';
    if (col.url) iframe.src = buildEmbedUrl(col.url);

    content.appendChild(inputArea);
    content.appendChild(iframe);

    // gear + menu
    const gearContainer = document.createElement('div');
    gearContainer.className = 'gear-container';

    const gearBtn = document.createElement('button');
    gearBtn.className = 'gear-btn';
    gearBtn.title = 'Opciones';
    gearBtn.textContent = '⚙️';

    const menu = document.createElement('div');
    menu.className = 'menu hidden';
    const btnEdit = document.createElement('button');
    btnEdit.textContent = 'Editar el enlace de la columna';
    const btnReload = document.createElement('button');
    btnReload.textContent = 'Recargar el enlace de la columna';
    const btnDelete = document.createElement('button');
    btnDelete.textContent = 'Eliminar la columna';
    menu.append(btnEdit, btnReload, btnDelete);

    gearContainer.appendChild(gearBtn);
    gearContainer.appendChild(menu);
    content.appendChild(gearContainer);

    // resizer
    const resizer = document.createElement('div');
    resizer.className = 'resizer';

    colEl.appendChild(content);
    colEl.appendChild(resizer);
    // events
    // helper para obtener el índice actual de esta columna
    const getIndex = () => Number(colEl.dataset.index);

    showBtn.addEventListener('click', () => {
      const i = getIndex();
      const url = input.value.trim();
      if (!url) return;
      state.columns[i].url = url;
      saveState(state);
      iframe.src = buildEmbedUrl(url);
      // show iframe
      colEl.classList.add('has-url');
      inputArea.style.display = 'none';
      iframe.style.display = 'block';
    });

    gearBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      menu.classList.toggle('hidden');
    });

    btnEdit.addEventListener('click', () => {
      const i = getIndex();
      menu.classList.add('hidden');
      const current = state.columns[i].url || '';
      const next = window.prompt('Editar enlace de la columna:', current);
      if (next == null) return;
      const url = next.trim();
      state.columns[i].url = url;
      saveState(state);
      input.value = url;
      if (url) {
        iframe.src = buildEmbedUrl(url);
        colEl.classList.add('has-url');
        inputArea.style.display = 'none';
        iframe.style.display = 'block';
      } else {
        iframe.removeAttribute('src');
        colEl.classList.remove('has-url');
        inputArea.style.display = '';
        iframe.style.display = 'none';
      }
    });

    btnReload.addEventListener('click', () => {
      const i = getIndex();
      menu.classList.add('hidden');
      const url = state.columns[i].url;
      if (!url) return;
      iframe.src = buildEmbedUrl(url);
    });

    btnDelete.addEventListener('click', () => {
      const i = getIndex();
      menu.classList.add('hidden');

      // actualizar estado
      state.columns.splice(i, 1);
      if (state.columns.length > 0) setEqualWidths();
      saveState(state);

      // eliminar la columna del DOM
      colEl.remove();

      // reindexar columnas restantes y actualizar anchos sin recargar iframes
      const children = Array.from(elColumns.children);
      children.forEach((child, idx) => {
        child.dataset.index = String(idx);
        if (state.columns[idx]) {
          child.style.flexBasis = `${state.columns[idx].width}%`;
        }
      });
    });

    // resizing
    resizer.addEventListener('mousedown', (e) => {
      e.preventDefault();
      startResize(colEl, e);
    });

    // evitar duplicar append (se deja solo una vez)
    colEl.appendChild(content);
    colEl.appendChild(resizer);
    return colEl;
  }

  function startResize(colEl, downEvent) {
    const i = Array.prototype.indexOf.call(elColumns.children, colEl);
    if (i < 0) return;

    const containerRect = elColumns.getBoundingClientRect();
    const totalW = containerRect.width;
    const startX = downEvent.clientX;
    const leftW = state.columns[i].width;
    const rightW = state.columns[i + 1]?.width;
    if (rightW == null) return;

    document.body.classList.add('dragging');

    function onMove(e) {
      const dx = e.clientX - startX;
      const deltaPct = (dx / totalW) * 100;
      let newLeft = leftW + deltaPct;
      let newRight = rightW - deltaPct;
      const min = 10;
      if (newLeft < min) {
        newRight -= (min - newLeft);
        newLeft = min;
      }
      if (newRight < min) {
        newLeft -= (min - newRight);
        newRight = min;
      }
      newLeft = Math.max(min, newLeft);
      newRight = Math.max(min, newRight);

      state.columns[i].width = newLeft;
      state.columns[i + 1].width = newRight;

      const leftEl = elColumns.children[i];
      const rightEl = elColumns.children[i + 1];
      if (leftEl) leftEl.style.flexBasis = `${newLeft}%`;
      if (rightEl) rightEl.style.flexBasis = `${newRight}%`;
    }

    function onUp() {
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      document.body.classList.remove('dragging');
      const sum = state.columns.reduce((acc, c) => acc + c.width, 0);
      state.columns.forEach(c => c.width = c.width * (100 / sum));
      saveState(state);
    }

    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  }

  // --- NUEVAS FUNCIONES: añadir / exportar / importar configuración ---

  function addColumn() {
    // misma lógica que antes tenía el handler de elAdd
    state.columns.push({ url: '', width: 0 });
    setEqualWidths();
    saveState(state);

    // actualizar anchos de columnas ya existentes sin recrearlas
    for (let i = 0; i < state.columns.length - 1; i++) {
      const colEl = elColumns.children[i];
      if (colEl) colEl.style.flexBasis = `${state.columns[i].width}%`;
    }

    // crear y añadir solo la nueva columna
    const index = state.columns.length - 1;
    const newColEl = createColumnElement(state.columns[index], index);
    elColumns.appendChild(newColEl);
  }

  function exportConfig() {
    const data = { columns: state.columns };
    const json = JSON.stringify(data, null, 2);
    try {
      const blob = new Blob([json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'multichat-config.json';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch {
      // fallback simple si Blob/URL fallan
      window.prompt('Copia la configuración JSON:', json);
    }
  }

  function importConfig() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/json';
    input.addEventListener('change', () => {
      const file = input.files && input.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const obj = JSON.parse(String(reader.result));
          if (!obj || !Array.isArray(obj.columns)) {
            alert('JSON no válido: falta "columns".');
            return;
          }
          state = {
            columns: obj.columns.map(c => ({
              url: typeof c.url === 'string' ? c.url : '',
              width: Number(c.width) || 0,
            })),
          };

          if (state.columns.length === 0) {
            // si viene vacío, dejamos al menos columnas con ancho igualado
            setEqualWidths();
          } else {
            const sum = state.columns.reduce((acc, c) => acc + (c.width || 0), 0);
            if (sum > 0) {
              state.columns.forEach(c => c.width = (c.width || 0) * (100 / sum));
            } else {
              setEqualWidths();
            }
          }

          saveState(state);
          render();
        } catch {
          alert('No se pudo leer el JSON.');
        }
      };
      reader.readAsText(file);
    });
    input.click();
  }

  function createGlobalMenu() {
    globalMenu = document.createElement('div');
    globalMenu.className = 'menu global-menu hidden';

    const btnAdd = document.createElement('button');
    btnAdd.textContent = 'Añadir columna';
    const btnExport = document.createElement('button');
    btnExport.textContent = 'Exportar configuración';
    const btnImport = document.createElement('button');
    btnImport.textContent = 'Importar configuración';

    globalMenu.append(btnAdd, btnExport, btnImport);
    document.body.appendChild(globalMenu);

    btnAdd.addEventListener('click', (e) => {
      e.stopPropagation();
      globalMenu.classList.add('hidden');
      addColumn();
    });

    btnExport.addEventListener('click', (e) => {
      e.stopPropagation();
      globalMenu.classList.add('hidden');
      exportConfig();
    });

    btnImport.addEventListener('click', (e) => {
      e.stopPropagation();
      globalMenu.classList.add('hidden');
      importConfig();
    });
  }

  // Botón flotante: abre/cierra menú global (ya no añade directamente)
  elAdd.addEventListener('click', (e) => {
    e.stopPropagation();
    if (!globalMenu) createGlobalMenu();
    globalMenu.classList.toggle('hidden');
  });

  // click outside to close any open menu (incluye el global, que también tiene clase .menu)
  document.addEventListener('click', () => {
    document.querySelectorAll('.menu').forEach(m => m.classList.add('hidden'));
  });

  // Embed helpers for YouTube/Twitch chat + file:// notice
  const PARENT_DOMAIN = location.hostname || '';
  const IS_FILE = location.protocol === 'file:';
  const IS_INSECURE_FOR_TWITCH = location.protocol !== 'https:' && PARENT_DOMAIN !== 'localhost' && PARENT_DOMAIN !== '127.0.0.1';

  if (IS_FILE) {
    setTimeout(() => {
      alert('Para embeber chats de YouTube/Twitch abre con http:// (p.ej. http://localhost). file:// no funciona con embed_domain/parent.');
    }, 0);
  }

  // Banner global de aviso para Twitch sobre HTTPS
  function ensureTwitchHttpsBanner() {
    if (!IS_INSECURE_FOR_TWITCH) return;
    if (document.querySelector('.env-warning')) return;
    const div = document.createElement('div');
    div.className = 'env-warning';
    div.innerHTML = `
      <button class="close" title="Cerrar">✕</button>
      Twitch bloquea el chat en orígenes sin HTTPS. Abre esta página en:
      <b>https://</b> (con certificado) o en <b>http://localhost</b>/<b>http://127.0.0.1</b>.
      <br/>Host actual: <code>${PARENT_DOMAIN}</code>
    `;
    div.querySelector('.close')?.addEventListener('click', () => div.remove());
    document.body.appendChild(div);
  }

  function isIPv4Host(host) {
    return /^\d{1,3}(?:\.\d{1,3}){3}$/.test(host);
  }

  function isIPv6Host(host) {
    // very loose IPv6 detection (acceptable for warning purposes)
    return host.includes(':');
  }

  function buildTwitchParentParams() {
    // Twitch allows multiple parent params. We'll include the current hostname
    // and common local dev hosts to reduce friction.
    const parents = new Set();
    if (PARENT_DOMAIN) parents.add(PARENT_DOMAIN);
    parents.add('localhost');
    parents.add('127.0.0.1');
    // ...si necesitas más, añádelos aquí...
    return Array.from(parents).map(p => `parent=${encodeURIComponent(p)}`).join('&');
  }

  function toYouTubeEmbed(raw) {
    try {
      const u = new URL(raw);
      const host = u.hostname.replace(/^www\./, '');
      let id = null;

      if (host === 'youtu.be') {
        id = u.pathname.split('/').filter(Boolean)[0] || null;
      } else if (host.endsWith('youtube.com')) {
        const parts = u.pathname.split('/').filter(Boolean);
        if (u.pathname === '/watch') id = u.searchParams.get('v');
        else if (parts[0] === 'embed' && parts[1]) id = parts[1];
        else if (parts[0] === 'live' && parts[1]) id = parts[1]; // best-effort
        else if (parts[0] === 'live_chat') id = u.searchParams.get('v');
      }

      if (!id || !PARENT_DOMAIN) return null;
      return `https://www.youtube.com/live_chat?v=${encodeURIComponent(id)}&embed_domain=${encodeURIComponent(PARENT_DOMAIN)}`;
    } catch {
      return null;
    }
  }

  let twitchHttpsWarned = false;
  function toTwitchEmbed(raw) {
    try {
      const u = new URL(raw);
      const host = u.hostname.replace(/^www\./, '');
      if (!host.endsWith('twitch.tv')) return null;

      const parts = u.pathname.split('/').filter(Boolean);
      let channel = null;

      if (parts.length === 1) channel = parts[0];                        // /{channel}
      else if (parts[0] === 'popout' && parts[2] === 'chat') channel = parts[1]; // /popout/{channel}/chat
      else if (parts[0] === 'embed' && parts[2] === 'chat') channel = parts[1];  // /embed/{channel}/chat
      if (!channel || !PARENT_DOMAIN) return null;

      // Aviso por usar HTTP fuera de localhost.
      if (IS_INSECURE_FOR_TWITCH && !twitchHttpsWarned) {
        twitchHttpsWarned = true;
        setTimeout(() => ensureTwitchHttpsBanner(), 0);
      }

      // Warn early if using an IP host, since Twitch commonly blocks IP-based parents unless HTTPS.
      if (isIPv4Host(PARENT_DOMAIN) || isIPv6Host(PARENT_DOMAIN)) {
        setTimeout(() => {
          alert('Twitch suele bloquear "parent" con IP si no usas HTTPS. Abre la página con un nombre de host (p. ej., http://localhost o un dominio con HTTPS) para que el chat se muestre.');
        }, 0);
      }

      const parentParams = buildTwitchParentParams();
      const query = parentParams ? `${parentParams}&theme_mode=dark` : 'theme_mode=dark';
      // return `https://www.twitch.tv/embed/${encodeURIComponent(channel)}/chat?${query}`;
      return `https://www.twitch.tv/embed/${encodeURIComponent(channel)}/chat?darkpopout&${parentParams}`; 
    } catch {
      return null;
    }
  }

  function buildEmbedUrl(raw) {
    const yt = toYouTubeEmbed(raw);
    if (yt) return yt;
    const tw = toTwitchEmbed(raw);
    if (tw) return tw;
    return raw; // fallback (puede bloquearse si el sitio no permite iframes)
  }

  // initial render
  ensureTwitchHttpsBanner();
  render();
})();
