// Tema claro ou escuro. Sem escolha guardada, a página segue o sistema, só
// com CSS. O botão guarda a escolha neste navegador.
(function () {
  var raiz = document.documentElement;
  var guardado = null;
  try { guardado = localStorage.getItem('tema'); } catch (erro) { /* sem armazenamento */ }
  if (guardado === 'claro' || guardado === 'escuro') raiz.dataset.tema = guardado;

  document.addEventListener('DOMContentLoaded', function () {
    var botao = document.getElementById('alternar-tema');
    if (!botao) return;
    // O botão nasce oculto: sem script ele não teria o que fazer.
    botao.hidden = false;
    botao.addEventListener('click', function () {
      var escuro = raiz.dataset.tema
        ? raiz.dataset.tema === 'escuro'
        : window.matchMedia('(prefers-color-scheme: dark)').matches;
      var novo = escuro ? 'claro' : 'escuro';
      raiz.dataset.tema = novo;
      try { localStorage.setItem('tema', novo); } catch (erro) { /* sem armazenamento */ }
    });
  });
})();
