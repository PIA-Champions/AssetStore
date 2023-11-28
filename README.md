# AssetStore
Uma loja de assets para atender produtores e desenvolvedores de jogos.

## Backend:

### User Table:

The "User" table manages user information within the system. Each user is uniquely identified by an ID generated based on their username. The table includes the following fields:
- **ID:** A unique identifier for each user, generated using a hashing function based on the user's name.
- **Name:** The username of the user.
- **Password:** The hashed and salted password of the user for secure authentication.
- **Balance:** Amout of credits disponible for purchasing 
- **Purchased Asset Packs:** A list of asset packs that the user has purchased. Each item on the list is an id for an asset_pack that is refferenced on the ***Asset pack table***.

    ```markdown
    ['item id','another item id', ...]
    
- **Hash:** The hash of the user's password for verification during login.
- **Salt:** The salt used during password hashing.
- **Rounds:** The number of rounds used during password hashing.
- **Hashed:** The final hashed password stored in the database.

### Asset Packs Table:

The "Asset Packs" table manages information about various asset packs available in the system. Each asset pack is uniquely identified by an ID generated based on its title. The table includes the following fields:

- **ID:** A unique identifier for each asset pack, generated using a hashing function based on the asset pack's title.
- **Title:** The title or name of the asset pack.
- **Description:** A brief description of the contents or purpose of the asset pack.
- **Cost:** The value of the packet, in credits 
- **Web Address:** The web address or URL associated with the asset pack.
- **Store Media List:** A list of dictionaries that describe media content that is used for presentation of the asset pack on the store. Each dictionary has the folowing format:

    ```markdown
    {'web_address':'The url for the media file','type':'tumbnail'} 
