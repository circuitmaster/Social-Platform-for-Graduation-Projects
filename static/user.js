var course_num = 0
var elems = new Array()

function add_course(){
	var value = document.getElementById("noc").value
	while(value != course_num){
		if(value<0) value=0
		if(value < course_num){
			var son = elems.pop()
			son.remove()
			course_num--
		}else{
			var para = document.createElement("input");
			var grade = document.createElement("input");
			para.className = 'input'
			para.type = 'text'
			para.name = 'course'
			para.placeholder = 'Enter ' + (course_num+1).toString() + 'th Course Name'
			grade.className = 'input'
			grade.type = 'text'
			grade.name = 'grade'
			grade.placeholder = 'Enter ' + (course_num+1).toString() + 'th Course Grade'

			var element = document.getElementById("div1");
			var child = document.getElementById("p1");
			element.insertBefore(para,child);
			element.insertBefore(grade,child);
			elems.push(para)
			course_num++
		}
	}
}