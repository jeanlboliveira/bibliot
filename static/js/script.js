function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

const csrftoken = getCookie('csrftoken')

const fetchURL = (url) =>
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
      'X-CSRFToken': csrftoken,
    }
  })



function debounceEvent(fn, wait = 500) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
}


function atualizarCarrinho(data) {
  document.querySelector('.carrinho').textContent = data.quantidade_total_carrinho

}