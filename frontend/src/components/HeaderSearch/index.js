import styles from '../HeaderSearch/HeaderSearch.module.css'

function HeaderSearch() {
    return (        
        <div className={styles.searchBox}>
            <input className={styles.searchInput} type="text" name="" placeholder="Search"/>
            <button className={styles.searchButton} >
            <span class="material-icons">
                search
            </span>
            </button>
        </div>
    );
}

export default HeaderSearch;