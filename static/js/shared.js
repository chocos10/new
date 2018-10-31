function sortByName() {
  var main = document.getElementById( 'result' );

  [].map.call( main.children, Object ).sort( function ( a, b ) {
      var titleA = a.getAttribute('data-title').toUpperCase();
      var titleB = b.getAttribute('data-title').toUpperCase();
      return (titleA < titleB) ? -1 : (titleA > titleB) ? 1 : 0;
  }).forEach( function ( elem ) {
      main.appendChild( elem );
  });
}

function sortByPublishedAt() {
  var main = document.getElementById( 'result' );

  [].map.call( main.children, Object ).sort( function ( a, b ) {
      var dateA = a.getAttribute('data-published').toUpperCase();
      var dateB = b.getAttribute('data-published').toUpperCase();
      return (dateA < dateB) ? -1 : (dateA > dateB) ? 1 : 0;
  }).forEach( function ( elem ) {
      main.appendChild( elem );
  });
}

document.getElementById('sortBy').onchange=changeEventHandler;

function changeEventHandler(event) {
  var sortBy = event.target.value;
  console.log(sortBy);
  if (sortBy === 'title') {
    sortByName();
  } else if (sortBy === 'date') {
    sortByPublishedAt();
  }
}

