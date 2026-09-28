// Navegación: links "Nosotros","Publicaciones" y "Login"
// Script separado: comportamiento de los links del nav (Publicaciones / Login)
/*   (function () {
    const navLinks = document.querySelectorAll('.nav-actions > a[data-nav]');

    navLinks.forEach(link => {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const target = this.dataset.nav;

        if (target === 'publicaciones') {
          const catalogo = document.getElementById('catalogWrap');
          if (catalogo) catalogo.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        if (target === 'login') {
          alert('Abrir formulario de inicio de sesión.');
        }
      });
    });
  })();

// Catálogo: render dinámico de fichas de perros y gatos. Falta agregar uno o dos botones dentro de cada card 
const animals = [
    {id:'014-P', name:'Tobi',    tipo:'Perro', edad:'2 años',  tam:'Mediano', estado:'disponible', img:'https://placedog.net/380/300?id=1'},
    {id:'022-G', name:'Mora',    tipo:'Gato',   edad:'1 año',   tam:'Pequeño', estado:'disponible', img:'https://cataas.com/cat?width=380&height=300&type=square&r=1'},
    {id:'009-P', name:'Duna',    tipo:'Perro', edad:'4 años',  tam:'Grande',  estado:'adoptado',   img:'https://placedog.net/380/300?id=3'},
    {id:'031-G', name:'Café',    tipo:'Gato',   edad:'6 meses', tam:'Pequeño', estado:'disponible', img:'https://cataas.com/cat?width=380&height=300&type=square&r=2'},
    {id:'018-P', name:'Bruno',   tipo:'Perro', edad:'3 años',  tam:'Mediano', estado:'disponible', img:'https://placedog.net/380/300?id=5'},
    {id:'027-G', name:'Kiwi',    tipo:'Gato',   edad:'2 años',  tam:'Pequeño', estado:'disponible', img:'https://cataas.com/cat?width=380&height=300&type=square&r=3'},
    {id:'011-P', name:'Nala',    tipo:'Perro', edad:'5 años',  tam:'Grande',  estado:'adoptado',   img:'https://placedog.net/380/300?id=8'},
    {id:'035-G', name:'Simón',   tipo:'Gato',   edad:'1 año',   tam:'Mediano', estado:'disponible', img:'https://cataas.com/cat?width=380&height=300&type=square&r=4'},
    {id:'019-P', name:'Colita',  tipo:'Perro', edad:'8 meses', tam:'Pequeño', estado:'disponible', img:'https://placedog.net/380/300?id=11'},
    {id:'024-G', name:'Pepa',    tipo:'Gato',   edad:'3 años',  tam:'Mediano', estado:'disponible', img:'https://cataas.com/cat?width=380&height=300&type=square&r=5'},
    {id:'016-P', name:'Máximo',  tipo:'Perro', edad:'6 años',  tam:'Grande',  estado:'disponible', img:'https://placedog.net/380/300?id=13'},
    {id:'029-G', name:'Luna',    tipo:'Gato',   edad:'4 años',  tam:'Mediano', estado:'adoptado',   img:'https://cataas.com/cat?width=380&height=300&type=square&r=6'},
  ];

  const grid = document.getElementById('grid');

  function cardHTML(a){
    return `
      <article class="card" tabindex="0" aria-label="${a.name}, ${a.tipo}, ${a.edad}">
        <div class="card-photo">
          <img src="${a.img}" alt="${a.name}, ${a.tipo} en adopción" loading="lazy">
          <span class="stamp ${a.estado}">${a.estado === 'adoptado' ? 'Adoptado' : 'En adopción'}</span>
        </div>
        <div class="card-body">
          <div class="card-id mono">N.º ${a.id}</div>
          <div class="card-name">${a.name}</div>
          <div class="card-meta">
            <span>${a.tipo}</span><span class="dot">·</span>
            <span>${a.edad}</span><span class="dot">·</span>
            <span>${a.tam}</span>
          </div>
        </div>
      </article>`;
  }

  grid.innerHTML = animals.map(cardHTML).join('');

  const addCard = document.createElement('button');
  addCard.className = 'card card-add';
  addCard.setAttribute('aria-label', 'Publicar un nuevo expediente de adopción');
  addCard.innerHTML = `<span class="plus">+</span><span class="label">Publicar</span>`;
  addCard.addEventListener('click', () => {
    alert('Abrir formulario para publicar un nuevo perro o gato en adopción.');
  });
  grid.appendChild(addCard);

  document.getElementById('catalogCount').textContent = animals.length + ' expedientes'; */