document.addEventListener("DOMContentLoaded", function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const foodId = this.getAttribute('data-food-id');
            addToCart(foodId);
        });
    });

    function addToCart(foodId) {
        fetch('/add-to-cart/', {
            method: 'POST',
            body: JSON.stringify({ food_id: foodId }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // 获取 CSRF token
            }
        }).then(response => response.json())
        .then(data => {
            if(data.success) {
                alert("已添加到购物车!");
                // 这里可以添加更多的逻辑，比如更新页面上的购物车数量显示
            } else {
                alert("添加失败!");
            }
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
