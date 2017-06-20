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
        let url = window.location.origin + "/api/suggest/"+ query + "?format=json"; //TODO
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
            let url = window.location.origin + "/details/"+ sugg.id ;
            return <h5><li className="list-link"><a href={url}>{sugg.name}</a></li></h5>;
        });
        return (
            <div className={'search-box'}>
                <form className={'search-form'}>
                    <input className="form-control" placeholder='Search' ref="query" type="text" onChange={ (e) => this.updateSearch() }/>
                </form>
                <ul>
                    { suggestion }
                </ul>
            </div>
        );
    }
}

ReactDOM.render(<SearchBar context={window.props} />, document.getElementById('search-bar'));
