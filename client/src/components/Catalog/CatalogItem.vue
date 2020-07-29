<template>
    <div class="catalog-item">
        <p class="catalog-item__article grey" v-if="article.length > 0">
            Article: {{ this.article }}
        </p>
        <p class="catalog-item__title">
            {{ this.title }}
        </p>
        <p class="catalog-item__description">
            {{ this.description }}
        </p>
    </div>
</template>

<script>
    export default {
        name: "CatalogItem",
        props: {
            id: Number,
            images: Array,
            article: String,
            title: String,
            description: String
        },
        data() {
            return {}
        }
    }
</script>

<style scoped lang="scss">
    @import "../../styles/variables";

    .catalog-item {
        display: block;
        border: 1px solid $main-lightgrey;
        padding: 20px;

        &__article {
            margin: 20px 0;
        }

        &__title {
            font-size: 20px;
            line-height: 1.5;
            font-weight: 500;
        }

        &__description {
            margin-top: 17px;
        }
    }
</style>
