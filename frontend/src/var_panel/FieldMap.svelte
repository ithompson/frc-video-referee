<script lang="ts">
    import field_image from "../assets/2025-field.png";
</script>

<div class="field-map">
    <img src={field_image} alt="Field diagram" />
</div>

<style>
    .field-map {
        display: flex;
    }
    img {
        object-fit: contain;
        margin: auto;
        width: 440px;
    }
</style>
