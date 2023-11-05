import '../HeaderSearch/HeaderSearch.module.css'

function HeaderSearch() {
    return (
        <form className='form-search'>
            <input type="text" placeholder="Search assets" />
            <button type="submit">Search</button>
        </form>
    )
}

export default HeaderSearch;