<template>
    <div class="home">
        <div class="container">
            Homepage content
            <Catalog />
        </div>
    </div>
</template>

<script>
    import Catalog from "../components/Catalog/Catalog";

    export default {
        name: 'Home',
        components: {
            Catalog
        }
    }
</script>
