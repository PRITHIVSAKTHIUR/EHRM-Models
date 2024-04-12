document.addEventListener('DOMContentLoaded',()=>{
  const aboutButton = document.getElementById("Sign-in");
  const aboutButton1 = document.getElementById("Sign-in1");
  const cancelButton = document.getElementById("closebtn");
  const dialog = document.getElementById("Signin");
  


  // Update button opens a modal dialog
  aboutButton.addEventListener("click", () => {
    dialog.showModal();
  });


    // Update button opens a modal dialog
    aboutButton1.addEventListener("click", () => {
      dialog.showModal();
    });

  // Form cancel button closes the dialog box
  cancelButton.addEventListener("click", () => {
    dialog.close();
  })
});