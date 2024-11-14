const predefinedRooms = [
    "1A - CTE Math", "1AA - Direct Care Worker", "2A - Option Pathway", "3A - Success Lab", 
    "4A - Practical Nursing", "5A - Practical Nursing", "6A - Pre-Engineering / PLTW", 
    "7A - HVAC", "8A - Electrical", "9A - Certified Patient Care Technician", 
    "10A - Dental Assisting/Clinic", "11A - Masonry", "A Wing Hallway", "1B - Cafeteria", 
    "2B - ProStart", "3B - ProStart", "3BB - Masonry", "4B - Misc.", "4BB - SkillsUSA", 
    "5B - Carpentry", "6B - Welding", "8B - Carpentry Shop", "9B - Automotive", 
    "10B - Welding Shop", "11B - Collision Repair", "12B - Collision Repair Shop", 
    "13B - Cybersecurity", "14B - CTE English", "B Wing Hallway", "1C - Option Pathway", 
    "2C - Law and Public Safety", "3C - Plumbing", "4C - Diesel Technology", 
    "4CC - Diesel Technology Shop", "5C - Emergency and Firefighting Management Services", 
    "6C - Graphic Design / Multimedia Publishing", "7C - Medical Assisting", "C Wing Hallway", 
    "Lobby", "Office", "Commons"
];

const ip = "192.168.1.137"

const roomPicker = document.getElementById('roomPicker');
predefinedRooms.forEach(room => {
    const option = document.createElement('option');
    option.value = room;
    option.textContent = room;
    roomPicker.appendChild(option);
});

async function fetchEventInfo() {
    try {
        const response = await fetch('http://' + ip + ':8080/api/events');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const eventInfoDiv = document.getElementById('eventInfo');
        const roomsList = data.rooms.split(',').map(room => `<li>${room.trim()}</li>`).join('');
        eventInfoDiv.innerHTML = `
            <p><strong>Event Name:</strong> ${data.event_name}</p>
            <p><strong>Event Type:</strong> ${data.event_type}</p>
            <p><strong>Event Status:</strong> ${data.event_status}</p>
            <p><strong>Start Date:</strong> ${data.start_date}</p>
            <p><strong>End Date:</strong> ${data.end_date}</p>
            <p><strong>Rooms:</strong></p>
            <ul>${roomsList}</ul>
        `;
    } catch (error) {
        console.error('Error fetching event info:', error);
        document.getElementById('eventInfo').innerText = 'Error fetching event info.';
    }
}

document.getElementById('addRoomButton').addEventListener('click', function() {
    const selectedRoom = roomPicker.value;
    const roomList = document.getElementById('roomList');

    if (selectedRoom === "All Rooms") {
        predefinedRooms.forEach(room => {
            if (![...roomList.children].some(li => li.textContent === room)) {
                const listItem = document.createElement('li');
                listItem.textContent = room;
                roomList.appendChild(listItem);
            }
        });
    } else {
        if ([...roomList.children].some(li => li.textContent === selectedRoom)) {
            alert('Room already added.');
            return;
        }

        const listItem = document.createElement('li');
        listItem.textContent = selectedRoom;
        roomList.appendChild(listItem);
    }
});

document.getElementById('eventForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const roomList = document.getElementById('roomList');
    const rooms = [...roomList.children].map(li => li.textContent).join(',');

    const formData = {
        event_name: document.getElementById('eventName').value,
        event_type: document.getElementById('eventType').value,
        event_status: document.getElementById('eventStatus').value,
        start_date: document.getElementById('startDate').value,
        end_date: document.getElementById('endDate').value,
        rooms: rooms
    };

    try {
        const response = await fetch('http://' + ip + ':8080/api/events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('message').innerText = 'Event created successfully!';
    } catch (error) {
        console.error('Error submitting form:', error);
        document.getElementById('message').innerText = 'Error creating event.';
    }
});

document.getElementById('resetButton').addEventListener('click', async function(event) {
    event.preventDefault();
    try {
        await fetch('http://' + ip + ':8080/resetevent', {
            method: 'GET',
            headers: {
                'Content-Type': 'text/plain'
            }
        });
    } catch (error) {
        console.error("Error resetting event: " + error)
    }
});

document.getElementById('refreshButton').addEventListener('click', fetchEventInfo);
fetchEventInfo();
setInterval(fetchEventInfo, 1000);