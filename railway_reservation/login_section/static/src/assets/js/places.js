const createNumPlace = (counter) => {
    let placeContainer = document.getElementById('modalContainerNumPlace');
    // let placeContainer2 = document.getElementById('modalContainerNumPlace2') ;

    const div = document.createElement('div');
    div.setAttribute('class', 'flex justify-center');

    // const div2 = document.createElement('div');
    // div2.setAttribute('class', 'flex justify-center');

    // const input = document.createElement('input');
    const input = document.getElementById('seat_number_checkbox')
    input.setAttribute('type', 'checkbox');
    // input.setAttribute('name', 'place' + counter);
    input.setAttribute('value', counter);
    input.setAttribute('id', 'place' + counter);

    const label = document.createElement('label');
    label.setAttribute('for', 'place' + counter);
    label.setAttribute('class', ' rounded-lg hover:cursor-pointer hover:bg-gray-400 hover:text-white transition-colors text-center w-full bg-gray-300 text-gray-500 py-4');

    const labelText = document.createTextNode(counter);
    label.appendChild(labelText);


    div.appendChild(input);
    div.appendChild(label);
    placeContainer.appendChild(div);

    // div2.appendChild(input);
    // div2.appendChild(label);
    // placeContainer2.appendChild(div2);
}

for (let i = 1; i < 31; i++) {
    createNumPlace(i);
    // createNumPlaceForEdit(i);
}

