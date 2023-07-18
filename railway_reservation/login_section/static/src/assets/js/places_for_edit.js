const createNumPlaceForEdit = (counter) => {
    let placeContainer = document.getElementById('modalContainerNumPlace2');
    // let placeContainer2 = document.getElementById('modalContainerNumPlace2') ;

    const div = document.createElement('div');
    div.setAttribute('class', 'flex justify-center');

    // const div2 = document.createElement('div');
    // div2.setAttribute('class', 'flex justify-center');

    const input2 = document.createElement('input');
    // const input2 = document.getElementById('seat_number_checkbox2')
    input2.setAttribute('type', 'checkbox');
    input2.setAttribute('name', 'place' + counter);
    input2.setAttribute('value', counter);
    input2.setAttribute('id', 'place2' + counter);

    const label = document.createElement('label');
    // label.setAttribute('for', 'seat_number_checkbox2');
    label.setAttribute('for', 'place2' + counter);
    label.setAttribute('class', ' rounded-lg hover:cursor-pointer hover:bg-gray-400 hover:text-white transition-colors text-center w-full bg-gray-300 text-gray-500 py-4');

    const labelText = document.createTextNode(counter);
    label.appendChild(labelText);


    div.appendChild(input2);
    div.appendChild(label);
    placeContainer.appendChild(div);

    // div2.appendChild(input);
    // div2.appendChild(label);
    // placeContainer2.appendChild(div2);
}

for (let i = 1; i < 31; i++) {
    // createNumPlace(i);
    createNumPlaceForEdit(i);
}


