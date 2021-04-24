function insertIntoTextField(textField, value)
{
    let from = textField.selectionStart, to = textField.selectionEnd;
    let textBeforeValue = textField.value.slice(0, from), textAfterValue = textField.value.slice(to);
    textField.value = `${textBeforeValue}${value}${textAfterValue}`;
    textField.selectionStart = textField.selectionEnd = from + value.length;
    textField.focus();
}


function handleFile(input_element) {
    let file = input_element.files[0];
    let Placeholder = `img((${file.name}))`
    let reader = new FileReader();
    let data = document.querySelector('#data');
    let output = document.getElementById('text');
    reader.readAsDataURL(file);

    reader.onload = function() {
        insertIntoTextField(output, Placeholder);
        if (data.value == '') data.value = reader.result;
        else data.value += ` ${reader.result}`;
    };

    reader.onerror = function() {
        alert(reader.error);
    };
}
