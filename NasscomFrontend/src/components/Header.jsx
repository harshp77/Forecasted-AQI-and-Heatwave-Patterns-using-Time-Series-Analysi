import { images } from "../assets";

const { logo } = images;

function Header(){
  return (
    <header className="flex mt-12 justify-between items-center">
        <div className="header__logo">
            <img
                src={logo}
                width={200}
                height={55}
                alt="image"
            />
        </div>
        <div className="flex justify-between itmes-center">
            <div className="mx-4 text-text font-semibold"><button>Home</button></div>
            <div className="mx-4 text-text font-semibold"><button>About Us</button></div>
            <div className="mx-4 text-text font-semibold"><button>Services</button></div>
            <div className="mx-4 text-text font-semibold"><button>Pages</button></div>
            <div className="mx-4 text-text font-semibold"><button>Archive</button></div>
            <button className="mx-4 text-white bg-cta font-semibold h-8 w-20 rounded">Contact</button>
        </div>
    </header>
  );
}
export default Header;