function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function editNote(noteId) {

  window.location.href = "/edit-note?id="+noteId;
}


function updateNoteState(noteId) {
    fetch('/update-note-state', {
        method: "POST",
        body: JSON.stringify({ 'noteId': noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}


function editNote(noteId) {
    window.location.href = "/edit-note?id="+noteId;
}

