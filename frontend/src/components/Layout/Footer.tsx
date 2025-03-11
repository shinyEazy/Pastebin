const Footer = () => {
  return (
    <footer className="mt-auto py-6 bg-white text-gray-500 w-full">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm">
          PasteBin By SOA Group 1 • {new Date().getFullYear()}
        </p>
      </div>
    </footer>
  );
};

export default Footer;
