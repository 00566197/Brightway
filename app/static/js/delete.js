function deleteProduct(button) {
    const url = button.dataset.url;
   fetch(url, {
       method: "DELETE",
       headers: {
           "X-Requested-With": "XMLHttpRequest"
       }
   })
   .then(res => res.json())
   .then(data => {
       if (data.success) {
           // remove item from page
           button.closest('tr').remove();
       }
   })
   .catch(error => console.error(error));
}