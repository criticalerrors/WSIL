/**
 * Created by ddipa on 28/03/2017.
 */

const React = require('react');
const ReactDOM = require('react-dom');

class SearchBar extends React.Component {

    constructor(props) {
        super(props);
        this.state = {suggested: [] };
        this.search = this.search.bind(this);
        this.updateSearch = this.updateSearch.bind(this);
    }
    updateSearch() {
        this.search(this.refs.query.value);
    }

    search( query = '' ) {
        if (query == '') {
            this.setState({suggested: []});
            return;
        }
        let url = "http://" + window.location.hostname + ":8000/api/suggest/"+ query + "?format=json"; //TODO
        console.log(url);
        fetch(url)
            .then(function(data) {
                return data.json();
            })
            .then((jsonData)=>{
                this.setState({suggested: jsonData});
            })
            .catch((e) => {
                console.log(e);
            });
    }


    render() {
        let suggestion = this.state.suggested.map(function(sugg){
            let url = "http://" + window.location.hostname + ":8000/details/"+ sugg.name.toLowerCase() ;
            return <h5><li className="list-link"><a href={url}>{sugg.name}</a></li></h5>;
        });
        console.log(suggestion);
        return (
            <div className={'search-box'}>
                <form className={'search-form'}>
                    <input className="form-control" placeholder='ex: Ruby, Rails, Java, CSS, Javascript, Node, C#, SQL, etc.' ref="query" type="text" onChange={ (e) => this.updateSearch() }/>
                </form>
                <ul>
                    { suggestion }
                </ul>
            </div>
        );
    }
}

ReactDOM.render(<SearchBar context={window.props} />, document.getElementById('search-bar'));
