document.addEventListener("DOMContentLoaded", () => {

    const sections = document.querySelectorAll(".animate-on-scroll");

    const observer = new IntersectionObserver((entries)=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.classList.add("show");

            }

        });

    },{

        threshold:.15

    });

    sections.forEach(section=>{

        observer.observe(section);

    });

});