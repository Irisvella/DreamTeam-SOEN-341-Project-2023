const items = document.querySelectorAll('.item')
console.log(items.length)

const expand = (item, i) => {
  items.forEach((it, ind) => {
    if (i === ind) return
    it.clicked = false
  })
  gsap.to(items, {
    width: item.clicked ? '15vw' : '8vw',
    duration: 2,
    ease: 'elastic(1, .6)'
  })
  
  item.clicked = !item.clicked
  gsap.to(item, {
    width: item.clicked ? '42vw' : '15vw',
    duration: 2.5,
    ease: 'elastic(1, .3)'
  })
}

items.forEach((item, i) => {
  item.clicked = false
  item.addEventListener('click', () => expand(item, i))
})

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("page-loader").style.display = "none";
});


/****This js is to animate text on  homepage */

const observer = new IntersectionObserver((entries)=>{

  entries.forEach((entry) =>{
    if (entry.isIntersecting){
      entry.target.classList.add('show');
    }else{
      entry.target.classList.remove('show');
    }

  });
});

const dynamicText = document.querySelectorAll('.mb-4');
dynamicText.forEach((el)=> observer.observe(el));


/****dark theme */

function toggleDarkMode() {
  var body = document.body;
  body.classList.toggle("dark-mode");
  var isDarkMode = body.classList.contains("dark-mode");
  localStorage.setItem("isDarkMode", isDarkMode);
}


var themeIcon = document.getElementById("themeIcon");


themeIcon.onclick = function(){
  document.body.classList.toggle("dark-theme");
  if(document.body.classList.contains("dark-theme")){
    if(themeIcon.src.includes("sun.png")){
      themeIcon.src = "{{ url_for('static', filename='images/moon.png') }}";
      themeIcon.style.filter = "invert(1)";
    }
  }
  else{
    if(themeIcon.src.includes("moon.png")){
      themeIcon.src = "{{ url_for('static', filename='images/sun.png') }}";
      themeIcon.style.filter = "none";
    }
  }
}
