function alterando_data () {
          var data = document.getElementById("data_inicial").value
          document.getElementById("data_final").min = data
          document.getElementById("data_final").value = data
    }

function selecionando2 () {
        var id = document.getElementById("tipo").selectedIndex
        console.log(document.getElementById("arquivo"))
        //console.log(document.getElementById(id).options)
    }

function Modificando_min () {
          var data = document.getElementById("data_inicial").value
          document.getElementById("data_final").min = data

    }
