var stud_num = 0
var class_num = 0
var elems = new Array()
var elems2 = new Array()

function add_student(){
	var value = document.getElementById("nos").value
	while(value != stud_num){
		if(value>5) value=5
		if(value < stud_num){
			var son = elems.pop()
			son.remove()
			stud_num--
		}else{
			var para = document.createElement("input");
			para.className = 'input'
			para.type = 'text'
			para.name = 'contributer'
			para.placeholder = 'Enter ' + (stud_num+1).toString() + 'th Student Id'

			var element = document.getElementById("div1");
			var child = document.getElementById("p1");
			element.insertBefore(para,child);
			elems.push(para)
			stud_num++
		}
	}
}

function add_prereq(){
	var value = document.getElementById("noc").value
	while(value != class_num){
		if(value>5) value=5
		if(value < class_num){
			var son = elems2.pop()
			son.remove()
			class_num--
		}else{
			var para = document.createElement("input");
			para.className = 'input'
			para.type = 'text'
			para.name = 'prerequisite'
			para.placeholder = 'Enter ' + (class_num+1).toString() + 'th Class Name (Ex. BLG 317E)'

			var element = document.getElementById("div2");
			var child = document.getElementById("p2");
			element.insertBefore(para,child);
			elems2.push(para)
			class_num++
		}
	}
}