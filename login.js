function loguear()
{

let user=document.getElementById("email").value; 
let pass=document.getElementById("password").value; 

if(user=="admin@admin.com" && pass=="1234")
{
    window.location="gestion.html";

}
else
{
    alert("Datos incorrectos (admin@admin.com, pass 1234)")
}

}