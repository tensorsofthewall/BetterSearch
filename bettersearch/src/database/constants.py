# Types of files to parse
parsable_exts = {
    'mupdf': [
        'pdf','xps','fb2','epub',
        'mobi', 'xlsx', 'pptx'
    ],
    'ffmpeg_audio': [
        # Audio
        ".au",".it",".mak",".midi",
        ".kar",".mid",".mp4a",".mp3",
        ".ogg",".s3m",".tsp",".ts",
        ".qcp",".vox",".aif",".aiff",
        ".flac",".gsm",".aac",".jam",
        ".lam",".m4a",".mid",".mod",
        ".m4a",".mp3",".m3u",".xm",
        ".la",".ra",".ram",".sid",
        ".ra",".s3m",".vqe",".vqf",
        ".voc",".wav",".xex",".xex",
    ],
    'ffmpeg_image': [
        # Image
        ".bmp",".ras",".fif",".flo",
        ".g3",".gif",".heic",".ief",
        ".jpg",".jpeg",".jut",".nap",
        ".pic",".pct",".png",".svg",
        ".svg",".tiff",".tif",".psd",
        ".djvu",".djv",".fpx",".ico",
        ".rf",".rp",".wbmp",".xif",
        ".webp",".wmf",".3ds",".log",
        ".ras",".cur",".dwg",".eps",
        ".exr",".gem",".icns",".ico",
        ".art",".jps",".bmp",".niff",
        ".pcx",".pict",".pbm",".pgm",
        ".ppm",".qt",".rgb",".tga",
        ".tiff",".tif",".bmp",".xcf",
        ".xpm",".xwd",".orf",".nef",
        ".raf",".rw2",".dng",".cr2",
        ".crw",".raw",".dcr",".k25",
        ".kdc",".mrw",".pef",".x3f",
        ".arw",".sr2",".srf",".erf",    
    ],
    'ffmpeg_video': [
        # Video
        ".afl",".avi",".avs",".ts",
        ".mp4",".mpeg",".mpg",".mov",
        ".vdo",".viv",".rv",".vos",
        ".webm",".xdr",".xsr",".3df",
        ".dl",".dv",".fli",".flv",
        ".f4v",".jng",".m4v",".mkv",
        ".mng",".mjpg",".asf",".avi",
        ".qtc",".movie"
    ],
    'text': [
        ".asp",".css",".html",".htm",
        ".js",".mcf",".pas",".pgp",
        ".txt",".py",".csv",".coffee",
        ".rtx",".rtf",".sct",".tsv",
        ".t",".uri",".abc",".flx",
        ".wmls",".wml",".html",".a68",
        ".asm",".aip",".awk",".bcpl",
        ".c",".cpp",".htc",".diff",
        ".f",".java",".la",".lsp",
        ".m4",".mak",".xml",".m",
        ".bat",".reg",".m",".p",
        ".pl",".php",".po",".py",
        ".rb",".sass",".scss",".html",
        ".etx",".sgml",".sh",".spc",
        ".tcl",".tex",".uil",".uu",
        ".vcs",".vcf"    
    ]
}


# Table Creation constants
file_metadata_create = '''
CREATE TABLE IF NOT EXISTS file_metadata (
            file_id INTEGER PRIMARY KEY,
            file_path TEXT UNIQUE,
            file_name TEXT,
            file_size INTEGER,
            date_created TEXT,
            date_modified TEXT,
            date_accessed TEXT
        )'''

content_index_create = '''
CREATE TABLE IF NOT EXISTS content_index (
            file_id INTEGER,
            content TEXT,
            FOREIGN KEY (file_id) REFERENCES file_metadata(file_id)
            ON DELETE CASCADE
        )'''

image_metadata_create = '''
CREATE TABLE IF NOT EXISTS image_metadata (
            file_id INTEGER,
            dimensions TEXT,
            camera_model TEXT,
            date_taken TEXT,
            gps_coordinates TEXT,
            FOREIGN KEY (file_id) REFERENCES file_metadata(file_id) 
            ON DELETE CASCADE
        )'''


music_metadata_create = '''
CREATE TABLE IF NOT EXISTS music_metadata (
            file_id INTEGER,
            title TEXT,
            album TEXT,
            artist TEXT,
            genre TEXT,
            duration TEXT,
            FOREIGN KEY (file_id) REFERENCES file_metadata(file_id) 
            ON DELETE CASCADE
        )'''
        
video_metadata_create = '''
CREATE TABLE IF NOT EXISTS video_metadata (
            file_id INTEGER,
            title TEXT,
            duration TEXT,
            frame_rate TEXT,
            dimensions TEXT,
            director TEXT,
            FOREIGN KEY (file_id) REFERENCES file_metadata(file_id) 
            ON DELETE CASCADE
        )'''
        
email_metadata_create = '''
CREATE TABLE IF NOT EXISTS email_metadata (
            file_id INTEGER,
            subject TEXT,
            sender TEXT,
            recipients TEXT,
            date_sent TEXT,
            date_received TEXT,
            attachments TEXT,
            FOREIGN KEY (file_id) REFERENCES file_metadata(file_id) 
            ON DELETE CASCADE
        )'''
        
        
application_metadata_create = '''
CREATE TABLE IF NOT EXISTS application_metadata (
            file_id INTEGER,
            application_name TEXT,
            version TEXT,
            publisher TEXT,
            install_date TEXT,
            FOREIGN KEY (file_id) REFERENCES file_metadata(file_id) 
            ON DELETE CASCADE
        )'''


index_maintenance_create = '''
CREATE TABLE IF NOT EXISTS index_maintenance (
            task_id INTEGER PRIMARY KEY,
            task_type TEXT,
            file_id INTEGER,
            status TEXT,
            timestamp TEXT,
            FOREIGN KEY (file_id) REFERENCES file_metadata(file_id) 
            ON DELETE CASCADE
        )'''
        
        
# Win Search Index constants
WIN_CONN_STRING = 'Provider=Search.CollatorDSO;' \
              'Extended Properties=\"Application=Windows\"'
              
WIN_SYSTEMINDEX_COLS = {
    "author": "System.ItemAuthors",
    "date": "System.ItemDate",
    "date_modified": "System.DateModified",
    "date_accessed": "System.DateAccessed",
    # The extension of a file, without the dot at
    # the beginning
    "fileext": "System.ItemType",
    "path": "System.ItemPathDisplay",
    # Windows Search intern rank of the file
    "rank": "System.Search.Rank",
    # Mimetype of a file
    "mimetype": "MimeType",
    "url": "System.ItemUrl",
    # Filename: Same like os.path.basename(path)
    "name": "System.ItemName",
    # Size of a file in Bytes
    "size": "System.Size",
    # unknowen function
    "kind": "System.Kind",
    # ...more...
}

# Schema description
WIN_SYSTEMINDEX_SCHEMA_DESCRIPTION = {
    "author": "List of authors associated with a file.",
    "date": "Primary date and time of interest for an item. Usually signifies date and time of creation.",
    "date_modified": "The date and time the file was last modified.",
    "date_accessed": "The date and time the file was last opened.",
    "fileext": "Signifies type of file by extension, including leading period.",
    "path": "Full path of a file, which is unique.",
    "rank": "Relevance rank of a file. Used only for retrieval, not search.",
    "mimetype": "MIME type of the file.",
    "url": "Specifies URL of the file.", 
    "name": "Name of the file.",
    "size": "Size of the file in bytes.",
    "kind": "Categorizes the item into a broad type (e.g., document, music, picture, video).",
}

# SystemIndex Table Info for LLM
WIN_SYSTEMINDEX_TABLE_INFO = '''
CREATE TABLE SystemIndex (
    author TEXT,
    date DATETIME,
    date_modified DATETIME,
    date_accessed DATETIME,
    fileext VARCHAR(255),
    path TEXT UNIQUE,
    rank INT,
    mimetype VARCHAR(255),
    url VARCHAR(255),
    name VARCHAR(255),
    size BIGINT,
    kind VARCHAR(255)
)
'''